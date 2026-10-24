"""Interactive card and load planner for the Mandi desk. Pure functions, no network."""
import json
import math
import re
from datetime import datetime, timezone
from uuid import uuid4

from uagents_core.contrib.protocols.chat import ChatMessage, MetadataContent, TextContent

from mandi.core import Assumptions
from mandi.ranking import Result

TRUCK_QTL = 100.0  # ASSUMPTION: one truck carries 10 tonnes (100 quintals); editable in plan_load()


def selection_for(r: Result, rank_index: int, commodity: str, origin: str, mode: str, quintals: float | None) -> dict:
    """What ASI:One sends back when the user taps 'Plan this load' (all values must be JSON-safe)."""
    return {
        "action": "plan_load", "rank": rank_index, "market": r.market, "district": r.district, "state": r.state,
        "crop": commodity, "origin": origin, "mode": mode, "quintals": quintals, "net": round(r.net, 1),
    }


def build_card_payload(results: list[Result], commodity: str, origin: str, mode: str, quintals: float | None,
                       top: int = 5) -> dict:
    buy = mode == "buy"
    items = []
    for i, r in enumerate(results[:top], 1):
        badges = []
        if i == 1:
            badges.append({"type": "badge", "label": "Cheapest landed" if buy else "Best net", "variant": "success"})
        if r.approx:
            badges.append({"type": "badge", "label": "distance approximate", "variant": "warning"})
        children = [
            {"type": "heading", "value": f"{i}. {r.market}", "level": 3},
            {"type": "text", "value": f"{r.district}, {r.state}", "style": "muted"},
        ]
        if badges:
            children.append({"type": "group", "direction": "row", "gap": 8, "children": badges})
        children += [
            {"type": "text", "value": f"Price Rs {r.modal_price:,.0f}/qtl  |  {r.distance_km:.0f} km  |  "
                                      f"{r.drive_hours:.1f} h drive", "style": "body"},
            {"type": "text", "value": f"You {'pay' if buy else 'clear'}: Rs {r.net:,.0f} per quintal",
             "style": "emphasis"},
            {"type": "button", "label": "Plan this load", "primary": i == 1,
             "action": {"selection": selection_for(r, i - 1, commodity, origin, mode, quintals)}},
        ]
        items.append({"children": children})
    title = f"{commodity}: cheapest mandis to buy from" if buy else f"{commodity}: best mandis to sell at"
    return {"root": {"type": "section", "title": title, "subtitle": f"From {origin}, today's real prices",
                     "children": [{"type": "list", "items": items}]}}


def card_message(narration: str, payload: dict) -> ChatMessage:
    """One text bubble plus an interactive card declaration (no end-session: the user may tap a button)."""
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[
            TextContent(type="text", text=narration),
            MetadataContent(
                type="metadata",
                metadata={
                    "card_protocol_version": "1",
                    "requires_card_interaction": "true",
                    "card_kind": "custom",
                    "card_payload": json.dumps(payload),
                    "preferred_drawer_width_px": "540",
                },
            ),
        ],
    )


def parse_selection(text: str) -> dict | None:
    """A card tap arrives as JSON text when the user @mentions the agent directly."""
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return None
    return data if isinstance(data, dict) and data.get("action") == "plan_load" else None


def find_tap(text: str, last: dict | None) -> int | None:
    """Index into the last ranking for a 'Plan this load' tap, or None if the text is not a tap.

    Direct @mention: the selection arrives as JSON. Planner-mediated: ASI:One summarises it in prose
    that names the mandi, so match a market name from the last ranking next to a selection word.
    """
    if not last:
        return None
    results = last["results"]
    sel = parse_selection(text)
    if sel:
        idx = sel.get("rank")
        ok = isinstance(idx, int) and 0 <= idx < len(results) and results[idx].market == sel.get("market")
        return idx if ok else None
    low = text.lower()
    if not re.search(r"plan (this|the|my) load|plan load|load plan|plan_load|selected|picked|chose|choose|tapped|clicked", low):
        return None
    hits = [i for i, r in enumerate(results) if r.market.lower() in low]
    return hits[0] if len(hits) == 1 else None


def plan_load(results: list[Result], chosen: int, quintals: float | None, a: Assumptions, mode: str,
              truck_qtl: float = TRUCK_QTL) -> str:
    """Trip plan for the chosen mandi, plus an optional spread across the top three to hedge price risk."""
    buy = mode == "buy"
    assumed = quintals is None
    q = quintals if quintals else truck_qtl
    sel = results[chosen]
    trucks = max(1, math.ceil(q / truck_qtl))
    word = "pay" if buy else "clear"
    lines = [f"**Load plan: {sel.market} ({sel.district}, {sel.state})**\n"]
    if assumed:
        lines.append(f"_You did not say how much, so I assumed one full truck ({truck_qtl / 10:g} tonnes)._\n")
    lines.append(f"- Quantity: {q:,.0f} quintals ({q / 10:,.1f} tonnes), about **{trucks} truck{'s' if trucks > 1 else ''}** "
                 f"of {truck_qtl / 10:g} tonnes")
    lines.append(f"- Trip: {sel.distance_km:.0f} km, about {sel.drive_hours:.1f} h each way"
                 f"{' (distance approximate)' if sel.approx else ''}")
    lines.append(f"- Freight for the whole load: about Rs {sel.transport * q:,.0f} "
                 f"(Rs {a.truck_rate_rs_per_tonne_km:g} per tonne-km)")
    lines.append(f"- You {word}: **Rs {sel.net * q:,.0f}** in total (Rs {sel.net:,.0f} per quintal)")

    top = results[:3]
    if trucks >= 2 and len(top) >= 2:
        alloc = [0] * len(top)
        for t in range(trucks):  # whole trucks, round-robin down the ranking
            alloc[t % len(top)] += 1
        remaining, rows, total = q, [], 0.0
        for r, n in zip(top, alloc):
            qty = min(remaining, n * truck_qtl)
            remaining -= qty
            if qty <= 0:
                continue
            total += r.net * qty
            rows.append(f"| {r.market} | {n} | {qty:,.0f} | {r.net:,.0f} | {r.net * qty:,.0f} |")
        all_in = sel.net * q
        lines.append("\n**Option: spread the trucks across the top mandis**\n")
        lines.append("| Mandi | Trucks | Quintals | Net Rs/qtl | Total Rs |")
        lines.append("|---|---|---|---|---|")
        lines += rows
        diff = total - all_in
        better = (diff < 0) if buy else (diff > 0)
        lines.append(f"\nSpread total: Rs {total:,.0f}, which is Rs {abs(diff):,.0f} "
                     f"{'better' if better else 'worse'} than sending everything to {sel.market}.")
        lines.append("_The dataset has no market-depth (arrival volume) figures, so a big load may move a small "
                     "mandi's price. Spreading is a price-risk choice here, not a calculated gain._")
    return "\n".join(lines)
