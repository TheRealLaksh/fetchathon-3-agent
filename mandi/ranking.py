"""Rank mandis by net rupees per quintal (seller) or landed cost (buyer). Pure functions, no network."""
from collections import defaultdict
from dataclasses import dataclass

from mandi.core import Assumptions, net_price

# State names spelled as the data.gov.in mandi dataset spells them.
ADJACENT = {
    "Haryana": {"Punjab", "Himachal Pradesh", "Uttarakhand", "Uttar Pradesh", "Rajasthan", "NCT of Delhi", "Delhi", "Chandigarh"},
    "Punjab": {"Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Rajasthan", "Chandigarh"},
    "NCT of Delhi": {"Haryana", "Uttar Pradesh"},
    "Delhi": {"Haryana", "Uttar Pradesh"},
    "Uttar Pradesh": {"Uttarakhand", "Haryana", "NCT of Delhi", "Delhi", "Rajasthan", "Madhya Pradesh", "Chattisgarh", "Bihar", "Himachal Pradesh"},
    "Rajasthan": {"Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Gujarat"},
    "Uttarakhand": {"Himachal Pradesh", "Uttar Pradesh", "Haryana"},
    "Himachal Pradesh": {"Punjab", "Haryana", "Uttarakhand", "Jammu and Kashmir", "Chandigarh"},
    "Madhya Pradesh": {"Rajasthan", "Uttar Pradesh", "Chattisgarh", "Maharashtra", "Gujarat"},
    "Gujarat": {"Rajasthan", "Madhya Pradesh", "Maharashtra"},
    "Maharashtra": {"Gujarat", "Madhya Pradesh", "Chattisgarh", "Telangana", "Karnataka"},
    "Bihar": {"Uttar Pradesh", "West Bengal", "Odisha"},
    "West Bengal": {"Bihar", "Odisha", "Assam"},
    "Karnataka": {"Maharashtra", "Telangana", "Andhra Pradesh", "Tamil Nadu", "Keralam"},
    "Tamil Nadu": {"Keralam", "Karnataka", "Andhra Pradesh"},
    "Keralam": {"Tamil Nadu", "Karnataka"},
    "Telangana": {"Maharashtra", "Karnataka", "Andhra Pradesh", "Chattisgarh", "Odisha"},
    "Andhra Pradesh": {"Telangana", "Karnataka", "Tamil Nadu", "Odisha", "Chattisgarh"},
    "Odisha": {"West Bengal", "Chattisgarh", "Andhra Pradesh", "Bihar", "Telangana"},
    "Chattisgarh": {"Madhya Pradesh", "Uttar Pradesh", "Maharashtra", "Odisha", "Telangana", "Andhra Pradesh"},
}


def search_states(origin_state: str | None) -> list[str]:
    """Origin state plus its neighbours, so we only geocode and route plausible markets."""
    if not origin_state:
        return []
    return sorted({origin_state} | ADJACENT.get(origin_state, set()))


@dataclass
class Result:
    market: str
    district: str
    state: str
    modal_price: float  # mean modal price across varieties at this market today
    varieties: int
    arrival_date: str
    distance_km: float
    drive_hours: float
    transport: float
    spoilage: float
    fees: float
    approx: bool  # location is the district centre, so distance is approximate
    net: float  # seller: net Rs/qtl. buyer: landed Rs/qtl (lower is better)


def group_markets(rows) -> dict:
    """One entry per market: mean modal price over its varieties/grades, plus the latest date."""
    g = defaultdict(list)
    for r in rows:
        g[(r.market, r.district, r.state)].append(r)
    out = {}
    for key, rs in g.items():
        out[key] = (sum(x.modal_price for x in rs) / len(rs), len(rs), max(x.arrival_date for x in rs))
    return out


def rank(rows, routes, commodity: str, mode: str, a: Assumptions) -> list[Result]:
    """Seller: highest net first. Buyer: lowest landed cost first."""
    markets = group_markets(rows)
    results = []
    for rt in routes:
        key = (rt.market, rt.district, rt.state)
        if key not in markets:
            continue
        modal, n, date = markets[key]
        transport, spoilage, fees, net = net_price(modal, rt.distance_km, rt.drive_hours, commodity, a)
        if mode == "buy":
            net = modal + transport + spoilage  # the buyer pays freight and absorbs transit loss; fees are the seller's
            fees = 0.0
        results.append(Result(rt.market, rt.district, rt.state, modal, n, date, rt.distance_km, rt.drive_hours,
                              transport, spoilage, fees, rt.approx, net))
    results.sort(key=lambda r: r.net, reverse=(mode != "buy"))
    return results


def format_reply(results: list[Result], commodity: str, origin: str, mode: str, quintals: float | None,
                 a: Assumptions, skipped: int, top: int = 6) -> str:
    if not results:
        return (f"I found no {commodity} prices I could route from {origin} today. "
                "Try another crop or a nearby city.")
    buy = mode == "buy"
    best = results[0]
    by_sticker = sorted(results, key=lambda r: r.modal_price, reverse=not buy)[0]
    if buy:
        head = f"**{commodity}: cheapest mandi to buy from, for a buyer in {origin} (today's real prices)**\n"
    else:
        head = f"**{commodity}: best mandi to sell at from {origin} (today's real prices)**\n"
    lines = [head]
    col = "You pay (landed)" if buy else "You actually clear"
    lines.append(f"| # | Mandi | Price Rs/qtl | Road km | Drive h | {col} Rs/qtl |")
    lines.append("|---|---|---|---|---|---|")
    for i, r in enumerate(results[:top], 1):
        lines.append(f"| {i} | {r.market} ({r.district}, {r.state}) | {r.modal_price:,.0f} | {'~' if r.approx else ''}{r.distance_km:.0f} | "
                     f"{r.drive_hours:.1f} | **{r.net:,.0f}** |")
    verb = "cheapest landed" if buy else "highest net"
    lines.append(f"\n**Recommendation:** {best.market} gives the {verb} result at Rs {best.net:,.0f} per quintal.")
    if by_sticker.market != best.market:
        lines.append(f"Note: {by_sticker.market} has the {'lowest' if buy else 'highest'} sticker price "
                     f"(Rs {by_sticker.modal_price:,.0f}), but distance and spoilage change the order.")
    if quintals and len(results) > 1:
        last = results[:top][-1]
        gain = abs(best.net - last.net) * quintals
        lines.append(f"For {quintals:,.0f} quintals, picking {best.market} over the last option shown "
                     f"is a difference of about Rs {gain:,.0f}.")
    lines.append(
        f"\n_Prices: data.gov.in daily mandi data dated {best.arrival_date} (mean of today's varieties per mandi). "
        f"Distances: real road routes (OpenStreetMap/OSRM). Assumptions you can change: truck Rs "
        f"{a.truck_rate_rs_per_tonne_km:g} per tonne-km, mandi commission {a.commission_pct:g}%, spoilage "
        f"{a.spoilage_pct_per_hour.get(commodity.lower(), a.spoilage_pct_per_hour['default']):g}% of value per drive hour._")
    if any(r.approx for r in results[:top]):
        lines.append("_~ means the mandi's exact spot was not found, so the district centre was used (distance approximate)._")
    if skipped:
        lines.append(f"_{skipped} {'market was' if skipped == 1 else 'markets were'} skipped (outside {a.max_radius_km:.0f} km or could not be located)._")
    return "\n".join(lines)
