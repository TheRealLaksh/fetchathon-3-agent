"""Mandi Net-Price Desk: the ASI:One-facing agent.

Understands a trader's question with the ASI1 LLM, asks the Price agent and the Logistics agent
(separate agents) for real data, ranks mandis by net rupees per quintal and replies in chat.

Run the other two first:  python -m mandi.price_agent   and   python -m mandi.logistics_agent
Then:  USE_MAILBOX=1 python -m mandi.front_agent   (same seed as the earlier test agent, so the
Agentverse mailbox that is already connected keeps working).
"""
import asyncio
import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from uagents import Agent, Context, Protocol
from uagents.crypto import Identity
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

from mandi.core import Assumptions
from mandi.extras import build_card_payload, card_message, find_tap, parse_selection, plan_load
from mandi.models import Place, PriceReply, PriceRequest, RouteReply, RouteRequest
from mandi.ranking import ADJACENT, format_reply, rank, search_states

load_dotenv()

SEED = os.environ["AGENT_SEED_PHRASE"]
PRICE = Identity.from_seed(SEED + "-price", 0).address
LOGISTICS = Identity.from_seed(SEED + "-logistics", 0).address
USE_MAILBOX = os.environ.get("USE_MAILBOX") == "1"
MAX_MARKETS = 30  # geocoding is rate-limited (1/s); results are cached on disk after the first run
LAST: dict = {}  # sender -> last ranking, so a tap on a card button can be answered (lost on restart)

llm = OpenAI(base_url="https://api.asi1.ai/v1", api_key=os.environ["ASI1_API_KEY"])
STATE_NAMES = ", ".join(sorted(set(ADJACENT) | {s for v in ADJACENT.values() for s in v} - {"Delhi"}))

EXTRACT_PROMPT = f"""You read a message from a produce trader in India and return ONLY a JSON object, no prose:
{{"intent": "sell" | "buy" | "other", "commodity": string|null, "origin": string|null,
  "origin_state": string|null, "quantity_quintals": number|null,
  "truck_rate_rs_per_tonne_km": number|null, "commission_pct": number|null, "market_fee_pct": number|null}}
- intent: sell = they have produce and want the best mandi to sell at; buy = they want the cheapest mandi to source from;
  other = not about mandi prices.
- commodity: singular English name in Title Case, e.g. Tomato, Onion, Potato, Banana, Cauliflower.
- origin: the city or town the produce is in or the buyer is in, e.g. "Gurugram, Haryana".
- origin_state: that place's state, spelled exactly as one of: {STATE_NAMES}.
- quantity_quintals: 1 tonne = 10 quintals; null if not given.
- truck_rate_rs_per_tonne_km, commission_pct, market_fee_pct: only if the user states their own freight rate
  (Rs per tonne per km), agent commission (%) or market fee (%); otherwise null.
Use null for anything not stated. Do not guess the crop or the place."""

HELP = (
    "I'm the **Mandi Net-Price Desk**. Tell me what you have or need, and where you are, for example:\n\n"
    "- *I have 8 tonnes of tomato in Gurugram. Where should I sell today?*\n"
    "- *Where is onion cheapest to buy for a restaurant in Delhi?*\n\n"
    "I rank real mandis by what you actually clear after transport, spoilage and fees, using today's government prices."
)

agent = Agent(
    name="Mandi Net-Price Desk",
    seed=SEED,
    port=8001,
    **({"mailbox": True} if USE_MAILBOX else {"endpoint": ["http://127.0.0.1:8001/submit"]}),
    publish_agent_details=True,
)
protocol = Protocol(spec=chat_protocol_spec)


def parse_request(text: str) -> dict:
    r = llm.chat.completions.create(
        model="asi1",
        messages=[{"role": "system", "content": EXTRACT_PROMPT}, {"role": "user", "content": text}],
        max_tokens=300,
    )
    raw = str(r.choices[0].message.content)
    m = re.search(r"\{.*\}", raw, re.S)
    return json.loads(m.group(0)) if m else {}


async def say(ctx: Context, to: str, text: str, end: bool = False):
    content = [TextContent(type="text", text=text)]
    if end:
        content.append(EndSessionContent(type="end-session"))
    await ctx.send(to, ChatMessage(content=content))


@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(acknowledged_msg_id=msg.msg_id))
    text = "".join(i.text for i in msg.content if isinstance(i, TextContent)).strip()

    last = LAST.get(sender)
    ctx.logger.info("incoming from %s: %r (have list: %s)", sender[:14], text[:400], bool(last))
    tapped = find_tap(text, last)  # a tap on a card's "Plan this load" button (JSON, or ASI:One's prose summary)
    if tapped is not None:
        await say(ctx, sender, plan_load(last["results"], tapped, last["quintals"], last["a"], last["mode"]),
                  end=True)
        return
    if parse_selection(text):  # a card tap whose list we no longer hold (agent restarted)
        await say(ctx, sender, "That list has expired. Ask me again, for example: "
                               "*I have 8 tonnes of tomato in Gurugram. Where should I sell today?*", end=True)
        return

    try:
        req = await asyncio.to_thread(parse_request, text)
    except Exception:
        ctx.logger.exception("could not parse the request")
        await say(ctx, sender, HELP, end=True)
        return

    commodity, origin = req.get("commodity"), req.get("origin")
    if req.get("intent") not in ("sell", "buy") or not commodity or not origin:
        missing = []
        if req.get("intent") in ("sell", "buy"):
            missing = [n for n, v in (("the crop", commodity), ("your city or town", origin)) if not v]
        extra = f"\n\nI still need: {' and '.join(missing)}." if missing else ""
        await say(ctx, sender, HELP + extra, end=True)
        return

    mode = req["intent"]
    origin_state = req.get("origin_state")
    states = search_states(origin_state)
    await say(ctx, sender, f"Checking today's {commodity} prices near {origin} and the real road routes. "
                           "This can take up to a minute the first time.")

    prices, _ = await ctx.send_and_receive(
        PRICE, PriceRequest(commodity=commodity, states=states), response_type=PriceReply, timeout=120)
    if not isinstance(prices, PriceReply) or prices.error or not prices.rows:
        why = prices.error if isinstance(prices, PriceReply) and prices.error else "no rows came back"
        await say(ctx, sender, f"I could not get today's {commodity} prices ({why}). Please try again, "
                               "or try another crop.", end=True)
        return

    # One candidate per market, capped so the first routing run stays within reach.
    seen, places = set(), []
    for r in prices.rows:
        key = (r.market, r.district, r.state)
        if key not in seen:
            seen.add(key)
            places.append(Place(market=r.market, district=r.district, state=r.state))
    places = places[:MAX_MARKETS]

    a = Assumptions()
    for field_name, lo, hi in (("truck_rate_rs_per_tonne_km", 0.5, 20.0), ("commission_pct", 0.0, 30.0),
                               ("market_fee_pct", 0.0, 15.0)):
        v = req.get(field_name)
        if isinstance(v, (int, float)) and lo <= v <= hi:  # ignore absurd values the user or LLM may give
            setattr(a, field_name, float(v))
    routes, _ = await ctx.send_and_receive(
        LOGISTICS, RouteRequest(origin=origin, places=places, max_radius_km=a.max_radius_km),
        response_type=RouteReply, timeout=300)
    if not isinstance(routes, RouteReply) or not routes.origin_found or not routes.routes:
        await say(ctx, sender, f"I could not place {origin} on the map or find routable markets for {commodity}. "
                               "Try a nearby larger town.", end=True)
        return

    results = rank(prices.rows, routes.routes, commodity, mode, a)
    qty = req.get("quantity_quintals") if isinstance(req.get("quantity_quintals"), (int, float)) else None
    body = format_reply(results, commodity, origin, mode, qty, a, routes.skipped)
    if prices.source == "snapshot":
        body += (f"\n_Live government prices were unreachable, so this uses the last saved snapshot "
                 f"({prices.fetched_at}). Treat it as possibly stale._")
    if routes.estimated:
        body += (f"\n_The routing service was unreachable for {routes.estimated} markets, so their distances "
                 "are straight-line estimates._")
    LAST[sender] = {"results": results, "quantity": qty, "quintals": qty, "a": a, "mode": mode}
    # Full table as a plain text message first, so the answer always arrives, then the interactive card.
    await say(ctx, sender, body)
    await ctx.send(sender, card_message("Tap **Plan this load** on a mandi for trucks and totals.",
                                        build_card_payload(results, commodity, origin, mode, qty)))


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
