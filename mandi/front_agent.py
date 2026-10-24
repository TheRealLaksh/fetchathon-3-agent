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
import sys

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

from mandi.branding import profile_kwargs
from mandi.conditions import agents_used_line, weather_line
from mandi.core import Assumptions
from mandi.extras import build_card_payload, card_message, find_tap, parse_selection, plan_load
from mandi.models import Place, PriceReply, PriceRequest, RouteReply, RouteRequest, WeatherReply, WeatherRequest
from mandi.personal import (
    clean_language, facts_text, grounded, is_forget, memory_line, merge_request, remember, why_messages,
)
from mandi.ranking import ADJACENT, format_reply, rank, search_states

load_dotenv()
# Hindi and Hinglish messages must not break on a Windows console that defaults to a legacy code page.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SEED = os.environ["AGENT_SEED_PHRASE"]
PRICE = Identity.from_seed(SEED + "-price", 0).address
LOGISTICS = Identity.from_seed(SEED + "-logistics", 0).address
WEATHER = Identity.from_seed(SEED + "-weather", 0).address
USE_MAILBOX = os.environ.get("USE_MAILBOX") == "1"
MAX_MARKETS = 30  # geocoding is rate-limited (1/s); results are cached on disk after the first run
LAST: dict = {}  # sender -> last ranking, so a tap on a card button can be answered (lost on restart)

llm = OpenAI(base_url="https://api.asi1.ai/v1", api_key=os.environ["ASI1_API_KEY"])
STATE_NAMES = ", ".join(sorted(set(ADJACENT) | {s for v in ADJACENT.values() for s in v} - {"Delhi"}))

EXTRACT_PROMPT = f"""You read a message from a produce trader in India (English, Hindi in Devanagari, or Hinglish) and
return ONLY a JSON object, no prose:
{{"intent": "sell" | "buy" | "other", "commodity": string|null, "origin": string|null,
  "origin_state": string|null, "quantity_quintals": number|null,
  "truck_rate_rs_per_tonne_km": number|null, "commission_pct": number|null, "market_fee_pct": number|null,
  "language": "en" | "hi" | "hinglish"}}
- intent: sell = they have produce and want the best mandi to sell at; buy = they want the cheapest mandi to source from;
  other = not about mandi prices.
- commodity: singular English name in Title Case, e.g. Tomato, Onion, Potato, Banana, Cauliflower
  (tamatar/टमाटर = Tomato, pyaz/प्याज़ = Onion, aloo/आलू = Potato, kela/केला = Banana, gobhi/गोभी = Cauliflower).
- origin: the city or town the produce is in or the buyer is in, in English, e.g. "Gurugram, Haryana".
- origin_state: that place's state, spelled exactly as one of: {STATE_NAMES}.
- quantity_quintals: 1 tonne = 10 quintals = 1000 kg (ton/टन/tonne); null if not given.
- truck_rate_rs_per_tonne_km, commission_pct, market_fee_pct: only if the user states their own freight rate
  (Rs per tonne per km), agent commission (%) or market fee (%); otherwise null.
- language: the language the message is written in.
Use null for anything not stated. Do not guess the crop or the place.
You are also given what we remember about this user. If the message is a short follow-up that changes only some
details (for example "what if I take 60 quintals", "same for onion", "use Delhi instead", "my truck costs Rs 4"),
set intent to the remembered intent and fill only what the message states; the caller fills the rest from memory.
If the message is a complete new request, use only the message."""

HELP = (
    "I'm the **Mandi Net-Price Desk**. Tell me what you have or need, and where you are, for example:\n\n"
    "- *I have 8 tonnes of tomato in Gurugram. Where should I sell today?*\n"
    "- *Where is onion cheapest to buy for a restaurant in Delhi?*\n\n"
    "I rank real mandis by what you actually clear after transport, spoilage and fees, using today's government prices. "
    "I remember your crop, place and cost settings, so you can follow up with *what if 60 quintals?* or *same for onion*.\n\n"
    "आप हिंदी में भी पूछ सकते हैं, जैसे: *मेरे पास गुरुग्राम में 25 टन टमाटर है, कहाँ बेचूँ?*"
)

CHECKING = {
    "en": "Checking today's {crop} prices near {place} and the real road routes. This can take up to a minute the first time.",
    "hi": "आज के {crop} के भाव और {place} से सड़क के असली रास्ते देख रहा हूँ। पहली बार में एक मिनट तक लग सकता है।",
    "hinglish": "Aaj ke {crop} ke bhaav aur {place} se sadak ke asli raaste dekh raha hoon. Pehli baar mein ek minute tak lag sakta hai.",
}

agent = Agent(
    name="Mandi Net-Price Desk",
    seed=SEED,
    port=8001,
    **({"mailbox": True} if USE_MAILBOX else {"endpoint": ["http://127.0.0.1:8001/submit"]}),
    publish_agent_details=True,
    **profile_kwargs(
        "agent-readme-front.md",
        "Ranks Indian mandis by net Rs per quintal after real road freight, spoilage and fees, using today's "
        "government prices. For sellers and buyers.",
    ),
)
protocol = Protocol(spec=chat_protocol_spec)


def parse_request(text: str, saved: dict | None = None) -> dict:
    memory = json.dumps({k: v for k, v in (saved or {}).items() if k != "language"}, ensure_ascii=False)
    r = llm.chat.completions.create(
        model="asi1",
        messages=[{"role": "system", "content": EXTRACT_PROMPT},
                  {"role": "user", "content": f"Remembered about this user: {memory}\nMessage: {text}"}],
        max_tokens=300,
    )
    raw = str(r.choices[0].message.content)
    m = re.search(r"\{.*\}", raw, re.S)
    return json.loads(m.group(0)) if m else {}


def _why_sync(results, mode: str, quintals, a, language: str) -> str | None:
    """Two plain sentences from the ASI1 model, built from the ranking numbers only (see mandi/personal.py)."""
    facts = facts_text(results, mode, quintals, a)
    r = llm.chat.completions.create(model="asi1", messages=why_messages(facts, language, mode), max_tokens=220,
                                    timeout=25)
    text = re.sub(r"\s+", " ", str(r.choices[0].message.content)).strip()
    return text if grounded(text, facts) else None  # a number or advice the data does not support: drop the line


async def weather_for(ctx: Context, places: list[str]):
    """Today's weather for the origin and the top mandis from the Weather Agent; None if it does not answer in time."""
    try:
        reply, _ = await ctx.send_and_receive(WEATHER, WeatherRequest(places=places), response_type=WeatherReply,
                                              timeout=25)
        if isinstance(reply, WeatherReply) and reply.items:
            return reply.items
    except Exception:
        ctx.logger.warning("no weather this time", exc_info=True)
    return None  # weather is a bonus; the ranking never waits on it


async def explain(ctx: Context, results, mode: str, quintals, a, language: str) -> str | None:
    try:
        return await asyncio.wait_for(asyncio.to_thread(_why_sync, results, mode, quintals, a, language), timeout=30)
    except Exception:
        ctx.logger.warning("no model-written explanation this time", exc_info=True)
        return None  # the table and the plain-code recommendation are the answer; this line is a bonus


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
    ctx.logger.info("incoming from %s: %s (have list: %s)", sender[:14], ascii(text[:400]), bool(last))
    tapped = find_tap(text, last)  # a tap on a card's "Plan this load" button (JSON, or ASI:One's prose summary)
    if tapped is not None:
        await say(ctx, sender, plan_load(last["results"], tapped, last["quintals"], last["a"], last["mode"]),
                  end=True)
        return
    if parse_selection(text):  # a card tap whose list we no longer hold (agent restarted)
        await say(ctx, sender, "That list has expired. Ask me again, for example: "
                               "*I have 8 tonnes of tomato in Gurugram. Where should I sell today?*", end=True)
        return

    profile_key = f"profile:{sender}"
    if is_forget(text):
        ctx.storage.set(profile_key, {})
        await say(ctx, sender, "Done. I have cleared what I remembered about you (crop, place and cost settings).",
                  end=True)
        return
    saved = ctx.storage.get(profile_key) or {}

    try:
        req = await asyncio.to_thread(parse_request, text, saved)
    except Exception:
        ctx.logger.exception("could not parse the request")
        await say(ctx, sender, HELP, end=True)
        return
    req, filled = merge_request(req, saved)  # a follow-up inherits crop, place, quantity and cost settings
    lang = clean_language(req.get("language"))
    if filled:
        ctx.logger.info("filled from memory: %s", filled)

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
    await say(ctx, sender, CHECKING[lang].format(crop=commodity, place=origin))

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
    wx_places = [origin] + [f"{r.district}, {r.state}, India" for r in results[:2]]
    wx_labels = [origin.split(",")[0].strip()] + [r.district for r in results[:2]]
    why, wx_items = await asyncio.gather(explain(ctx, results, mode, qty, a, lang), weather_for(ctx, wx_places))
    wx_line = weather_line(wx_items, wx_labels) if wx_items else None
    body = format_reply(results, commodity, origin, mode, qty, a, routes.skipped, why=why,
                        extras=[wx_line] if wx_line else None)
    used = agents_used_line(len(places), len(routes.routes), bool(wx_line), bool(why))
    if prices.source == "snapshot":
        body += (f"\n_Live government prices were unreachable, so this uses the last saved snapshot "
                 f"({prices.fetched_at}). Treat it as possibly stale._")
    if routes.estimated:
        body += (f"\n_The routing service was unreachable for {routes.estimated} markets, so their distances "
                 "are straight-line estimates._")
    saved = remember(saved, req)
    ctx.storage.set(profile_key, saved)  # survives restarts; one small profile per chat user
    note = memory_line(saved)
    if note:
        body += "\n" + note
    LAST[sender] = {"results": results, "quantity": qty, "quintals": qty, "a": a, "mode": mode}
    # Full table as a plain text message first, so the answer always arrives, then the interactive card.
    # Two messages with no overlap: the table first, then the card whose own text carries the recommendation, the
    # explanation, the assumptions and the memory note. (A live ASI:One view shows only the last message of a turn;
    # a reloaded or shared chat shows both.)
    lines = body.splitlines()
    table_rows = [i for i, ln in enumerate(lines) if ln.startswith("|")]
    split = table_rows[-1] + 1 if table_rows else 0
    if split:
        await say(ctx, sender, "\n".join(lines[:split]).strip())
    card_text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines[split:])).strip()
    await ctx.send(sender, card_message(card_text + "\n\n" + used + "\n\nTap **Plan this load** on a mandi for trucks and totals.",
                                        build_card_payload(results, commodity, origin, mode, qty)))


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
