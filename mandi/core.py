"""Mandi Net-Price Desk: the maths and the data calls (no agent code in here).

Real data: mandi prices (data.gov.in, needs DATA_GOV_IN_API_KEY), geocoding (OpenStreetMap
Nominatim) and road distance (OSRM). Assumptions (truck rate, spoilage, commission) are
editable defaults, shown to the user as assumptions, never presented as data.
"""
import json
import math
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx

MANDI_RESOURCE = "9ef84268-d588-465a-a308-a864a43d0070"  # daily mandi prices, Rs per quintal
UA = {"User-Agent": "fetchathon3-mandi-desk/0.1 (student hackathon project)"}
GEO_CACHE = Path(__file__).with_name("geocache.json")


@dataclass
class Assumptions:
    """Editable and shown on every answer. Defaults are placeholders to tune, not facts."""

    truck_rate_rs_per_tonne_km: float = 3.0  # ASSUMPTION: tune with a real freight quote
    commission_pct: float = 2.0  # ASSUMPTION: mandi commission and fees
    spoilage_pct_per_hour: dict = field(default_factory=lambda: {"default": 0.2})  # ASSUMPTION per crop
    max_radius_km: float = 300.0


@dataclass
class Quote:
    market: str
    district: str
    state: str
    arrival_date: str
    modal_price: float  # Rs per quintal
    distance_km: float = 0.0
    drive_hours: float = 0.0
    transport_per_qtl: float = 0.0
    spoilage_per_qtl: float = 0.0
    fees_per_qtl: float = 0.0
    net_price: float = 0.0


def haversine_km(a: tuple, b: tuple) -> float:
    (la1, lo1), (la2, lo2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(h))


def _load_cache() -> dict:
    try:
        return json.loads(GEO_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def geocode(query: str) -> tuple | None:
    """Look a place up on OpenStreetMap Nominatim (1 request/second policy), cached on disk."""
    cache = _load_cache()
    if query in cache:
        return tuple(cache[query]) if cache[query] else None
    r = httpx.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": query, "format": "json", "limit": 1, "countrycodes": "in"},
        headers=UA,
        timeout=20,
    )
    time.sleep(1.1)
    hits = r.json() if r.status_code == 200 else []
    cache[query] = [float(hits[0]["lat"]), float(hits[0]["lon"])] if hits else None
    GEO_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return tuple(cache[query]) if cache[query] else None


def road_route(a: tuple, b: tuple) -> tuple[float, float] | None:
    """Real road (km, hours) between two (lat, lon) points from OSRM, or None if unreachable."""
    url = f"https://router.project-osrm.org/route/v1/driving/{a[1]},{a[0]};{b[1]},{b[0]}"
    r = httpx.get(url, params={"overview": "false"}, headers=UA, timeout=20)
    data = r.json()
    if data.get("code") != "Ok":
        return None
    leg = data["routes"][0]
    return leg["distance"] / 1000.0, leg["duration"] / 3600.0


def fetch_prices(commodity: str, state: str | None = None, limit: int = 200) -> list[dict]:
    """Latest published mandi rows for a commodity (optionally one state). Needs the API key."""
    key = os.environ["DATA_GOV_IN_API_KEY"]
    params = {"api-key": key, "format": "json", "limit": limit, "filters[commodity]": commodity}
    if state:
        params["filters[state]"] = state
    r = httpx.get(f"https://api.data.gov.in/resource/{MANDI_RESOURCE}", params=params, headers=UA, timeout=40)
    r.raise_for_status()
    return r.json().get("records", [])


def net_price(modal: float, distance_km: float, drive_hours: float, commodity: str, a: Assumptions) -> tuple:
    """Return (transport, spoilage, fees, net), all Rs per quintal (100 kg)."""
    transport = a.truck_rate_rs_per_tonne_km * distance_km / 10.0  # 1 quintal = 0.1 tonne
    spoil_pct = a.spoilage_pct_per_hour.get(commodity.lower(), a.spoilage_pct_per_hour["default"]) * drive_hours
    spoilage = modal * spoil_pct / 100.0
    fees = modal * a.commission_pct / 100.0
    return transport, spoilage, fees, modal - transport - spoilage - fees
