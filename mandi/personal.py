"""Per-user memory, follow-up merging and the grounding check for the ASI1 'why this mandi' line.

Pure functions, no network, so they are covered by offline tests (python -m mandi.test_upgrades).
"""
import re
from typing import Iterable

# What the desk remembers for each chat user (stored in the agent's own storage, never shared):
PROFILE_FIELDS = ("commodity", "origin", "origin_state", "quantity_quintals")
SETTING_FIELDS = ("truck_rate_rs_per_tonne_km", "commission_pct", "market_fee_pct")
LANGUAGES = {"en": "English", "hi": "Hindi (Devanagari script)", "hinglish": "Hinglish (Hindi written in the Roman alphabet)"}

FORGET = re.compile(
    r"\b(forget (me|my|everything)|clear (my )?(memory|profile|settings)|reset (my )?(memory|profile|settings)"
    r"|bhool ja[oy]e?|yaad mat rakho)\b|मुझे भूल|याद मत रख",
    re.I,
)


def is_forget(text: str) -> bool:
    return bool(FORGET.search(text))


def clean_language(value) -> str:
    return value if value in LANGUAGES else "en"


def _crop_changed(req: dict, saved: dict) -> bool:
    new, old = req.get("commodity"), saved.get("commodity")
    return bool(new and old and str(new).lower() != str(old).lower())


def merge_request(req: dict, saved: dict | None) -> tuple[dict, list[str]]:
    """Fill what the user left out from what we remember.

    Returns (merged request, names of the fields that came from memory). A short follow-up such as
    "what if 60 quintals" or "same for onion" has no intent of its own, so it inherits the saved one.
    """
    saved = saved or {}
    merged = dict(req)
    filled: list[str] = []
    states = ("sell", "buy")
    stated = [k for k in PROFILE_FIELDS + SETTING_FIELDS if req.get(k) not in (None, "")]
    if merged.get("intent") not in states:
        if stated and saved.get("intent") in states:  # a follow-up that changes some details
            merged["intent"] = saved["intent"]
            filled.append("intent")
        else:
            return merged, filled  # not a mandi question: leave it alone
    if not merged.get("commodity") and saved.get("commodity"):
        merged["commodity"] = saved["commodity"]
        filled.append("crop")
    if not merged.get("origin") and saved.get("origin"):
        merged["origin"] = saved["origin"]
        filled.append("place")
        if not merged.get("origin_state") and saved.get("origin_state"):
            merged["origin_state"] = saved["origin_state"]  # the state belongs to the remembered place only
    if merged.get("quantity_quintals") in (None, "") and saved.get("quantity_quintals") and not _crop_changed(req, saved):
        merged["quantity_quintals"] = saved["quantity_quintals"]  # same load; a different crop is a different load
        filled.append("quantity")
    for k in SETTING_FIELDS:
        if merged.get(k) in (None, "") and saved.get(k) is not None:
            merged[k] = saved[k]
            filled.append(k)
    return merged, filled


def remember(saved: dict | None, req: dict) -> dict:
    """The profile to store after a successful answer: what this request used, on top of what we had."""
    out = dict(saved or {})
    if req.get("intent") in ("sell", "buy"):
        out["intent"] = req["intent"]
    if _crop_changed(req, out) and req.get("quantity_quintals") in (None, ""):
        out.pop("quantity_quintals", None)  # the remembered quantity was for the previous crop
    for k in PROFILE_FIELDS + SETTING_FIELDS:
        if req.get(k) not in (None, ""):
            out[k] = req[k]
    out["language"] = clean_language(req.get("language"))
    return out


def memory_line(saved: dict) -> str:
    bits = [f"{label} {saved[k]}" for k, label in (("commodity", "crop"), ("origin", "place")) if saved.get(k)]
    for k, label, unit in (("truck_rate_rs_per_tonne_km", "truck", "Rs {:g}/tonne-km"), ("commission_pct", "commission", "{:g}%"),
                           ("market_fee_pct", "market fee", "{:g}%")):
        if saved.get(k) is not None:
            bits.append(f"{label} " + unit.format(saved[k]))
    if not bits:
        return ""
    return (f"_Remembered for your next question: {', '.join(bits)}. "
            "You can say \"what if 60 quintals\" or \"same for onion\"; say \"forget me\" to clear this._")


# ---- grounding for the model-written explanation -------------------------------------------------

_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
# The government dataset holds only today's prices, so no timing advice or forecast may appear.
_TIMING = re.compile(r"\b(tomorrow|next week|next month|wait|hold off|forecast|predict\w*|expect\w*|trend|will (rise|fall|go up|go down))\b"
                     r"|कल|इंतज़ार|इंतजार|अनुमान|rukna|intezaar|kal ", re.I)


def numbers_in(text: str) -> set[float]:
    out = set()
    for m in _NUM.findall(text.translate(_DIGITS)):
        try:
            out.add(round(float(m.replace(",", "")), 2))
        except ValueError:
            pass
    return out


def grounded(text: str, facts: str, always_ok: Iterable[float] = (1, 2, 3)) -> bool:
    """True when every number in `text` appears in `facts` and the text gives no timing advice or forecast."""
    if not text.strip() or _TIMING.search(text):
        return False
    allowed = numbers_in(facts) | set(always_ok)
    return all(n in allowed for n in numbers_in(text))


def facts_text(results, mode: str, quintals: float | None, a, top: int = 3) -> str:
    """The only facts the model may use: the top rows, the nearest and the highest-sticker mandi, and the gaps."""
    buy = mode == "buy"
    label = "landed cost" if buy else "you clear"
    lines = []
    for i, r in enumerate(results[:top], 1):
        lines.append(
            f"{i}. {r.market} ({r.district}, {r.state}): price Rs {r.modal_price:,.0f}/qtl, road {r.distance_km:.0f} km, "
            f"drive {r.drive_hours:.1f} h, transport Rs {r.transport:,.0f}, transit loss Rs {r.spoilage:,.0f}, "
            f"fees Rs {r.fees:,.0f}, {label} Rs {r.net:,.0f}/qtl")
    if results:
        sticker = sorted(results, key=lambda r: r.modal_price, reverse=not buy)[0]
        nearest = sorted(results, key=lambda r: r.distance_km)[0]
        lines.append(f"{'Lowest' if buy else 'Highest'} sticker price: {sticker.market} at Rs {sticker.modal_price:,.0f}/qtl, "
                     f"{label} Rs {sticker.net:,.0f}/qtl.")
        lines.append(f"Nearest mandi: {nearest.market}, {nearest.distance_km:.0f} km, {label} Rs {nearest.net:,.0f}/qtl.")
    if len(results) > 1:
        # from the rounded figures the user sees, so the sentence adds up on screen
        lines.append(f"Gap between 1st and 2nd: Rs {abs(round(results[0].net) - round(results[1].net)):,.0f}/qtl.")
    if quintals and len(results) > 1:
        lines.append(f"Quantity: {quintals:,.0f} quintals.")
    lines.append(f"Assumptions: truck Rs {a.truck_rate_rs_per_tonne_km:g}/tonne-km, mandi fee {a.market_fee_pct:g}%, "
                 f"commission {a.commission_pct:g}%.")
    return "\n".join(lines)


def why_messages(facts: str, language: str, mode: str) -> list[dict]:
    lang = LANGUAGES[clean_language(language)]
    system = (
        "You explain a mandi ranking to an Indian trader in at most two short sentences. "
        "Use ONLY the facts given. Do not use any number that is not in the facts. Write numbers with ASCII digits. "
        "Do not predict prices, give timing advice or tell the user to wait. Do not name any mandi, crop or place that is "
        f"not in the facts. The user is a {'buyer' if mode == 'buy' else 'seller'}. Write in {lang}. Plain text, no markdown."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": "Facts:\n" + facts}]
