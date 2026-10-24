"""Mandi Net-Price Desk: the maths and the data calls (no agent code in here).

Real data: mandi prices (data.gov.in, needs DATA_GOV_IN_API_KEY), geocoding (OpenStreetMap
Nominatim) and road distance (OSRM). Assumptions (truck rate, spoilage, commission) are
editable defaults, shown to the user as assumptions, never presented as data.
"""
import json
import math
import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx

MANDI_RESOURCE = "9ef84268-d588-465a-a308-a864a43d0070"  # daily mandi prices, Rs per quintal
UA = {"User-Agent": "fetchathon3-mandi-desk/0.1 (student hackathon project)"}
GEO_CACHE = Path(__file__).with_name("geocache.json")


@dataclass
class Assumptions:
    """Editable and shown on every answer. Sources are listed in SOURCES.md."""

    # Freight: Rs 2.8-3.7 per tonne-km on long hauls (Business Standard/CMIE Apr 2024 per-km rates for
    # a 15 t truck; FR8 route quotes). Median ~3.0. Short hauls usually cost more per tonne-km.
    truck_rate_rs_per_tonne_km: float = 3.0
    # Haryana fruit/vegetable market fee 1% + Rural Development Fund 1% (Tribune, Feb 2024).
    market_fee_pct: float = 2.0
    # Arhtiya (commission agent) commission: no reliable single rate found, varies by state, crop and
    # who pays, so it is NOT included unless the user states one.
    commission_pct: float = 0.0
    # Transit loss as % of value per drive hour. Anchored to NABCONS 2022 (via Lok Sabha answer):
    # vegetable transport loss about 0.1-1.6% per trip, i.e. ~0.2%/h over a ~5 h trip. Tomato and onion
    # are scaled by their market-stage losses (3.25% vs 1.96%, NABCONS 2022). Potato: no crop figure, default.
    spoilage_pct_per_hour: dict = field(default_factory=lambda: {"tomato": 0.25, "onion": 0.15, "default": 0.2})
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
    hits = None
    for attempt in range(3):  # Nominatim rate-limits; back off and retry instead of caching a failure
        try:
            r = httpx.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": query, "format": "json", "limit": 1, "countrycodes": "in"},
                headers=UA,
                timeout=20,
            )
        except httpx.HTTPError:
            return None  # offline: places already in the cache still work, new ones are skipped
        time.sleep(1.1)
        if r.status_code == 200:
            hits = r.json()
            break
        time.sleep(3 * (attempt + 1))
    if hits is None:
        return None  # lookup failed: do not cache, so a later call can retry
    cache[query] = [float(hits[0]["lat"]), float(hits[0]["lon"])] if hits else None
    GEO_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return tuple(cache[query]) if cache[query] else None


ROUTE_CACHE = Path(__file__).with_name("routecache.json")
_route_lock = threading.Lock()
_routes: dict | None = None  # "lat,lon|lat,lon" -> [km, hours]; real OSRM answers only, kept on disk


def _route_key(a: tuple, b: tuple) -> str:
    return f"{a[0]:.3f},{a[1]:.3f}|{b[0]:.3f},{b[1]:.3f}"


def _route_cache() -> dict:
    global _routes
    if _routes is None:
        try:
            _routes = json.loads(ROUTE_CACHE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _routes = {}
    return _routes


def save_route_cache() -> None:
    with _route_lock:
        if _routes:
            ROUTE_CACHE.write_text(json.dumps(_routes), encoding="utf-8")


def road_route(a: tuple, b: tuple) -> tuple[float, float] | None:
    """Real road (km, hours) between two (lat, lon) points from OSRM, or None if unreachable.

    Answers are cached (roads between two fixed points do not change during a hackathon), so a repeat
    question costs no routing calls. Safe to call from several threads.
    """
    key = _route_key(a, b)
    with _route_lock:
        hit = _route_cache().get(key)
    if hit:
        return hit[0], hit[1]
    url = f"https://router.project-osrm.org/route/v1/driving/{a[1]},{a[0]};{b[1]},{b[0]}"
    r = httpx.get(url, params={"overview": "false"}, headers=UA, timeout=20)
    data = r.json()
    if data.get("code") != "Ok":
        return None
    leg = data["routes"][0]
    result = (leg["distance"] / 1000.0, leg["duration"] / 3600.0)
    with _route_lock:
        _route_cache()[key] = [result[0], result[1]]
    return result


def fetch_prices(commodity: str, state: str | None = None, limit: int = 200) -> list[dict]:
    """Latest published mandi rows for a commodity (optionally one state). Needs the API key."""
    key = os.environ["DATA_GOV_IN_API_KEY"]
    params = {"api-key": key, "format": "json", "limit": limit, "filters[commodity]": commodity}
    if state:
        params["filters[state]"] = state
    for attempt in range(3):  # the API sometimes times out; retry before giving up
        try:
            r = httpx.get(f"https://api.data.gov.in/resource/{MANDI_RESOURCE}", params=params, headers=UA, timeout=40)
            r.raise_for_status()
            return r.json().get("records", [])
        except httpx.TimeoutException:
            if attempt == 2:
                raise
    return []


SNAPSHOT_DIR = Path(__file__).with_name("snapshots")


def fetch_prices_with_source(commodity: str, state: str | None = None, limit: int = 1000) -> tuple[list[dict], dict]:
    """Live rows, also saved as a dated snapshot (history builds up day by day).

    If the live API fails, fall back to the last saved snapshot and say so in the returned info dict.
    """
    slug = commodity.lower().replace(" ", "_")
    try:
        rows = fetch_prices(commodity, state, limit)
    except Exception:
        rows = None
    if rows:
        if state is None:  # only whole-crop fetches are saved, so a snapshot can serve any state later
            payload = json.dumps({"fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"), "rows": rows})
            day_dir = SNAPSHOT_DIR / time.strftime("%Y-%m-%d")
            day_dir.mkdir(parents=True, exist_ok=True)
            (SNAPSHOT_DIR / f"{slug}.json").write_text(payload, encoding="utf-8")
            (day_dir / f"{slug}.json").write_text(payload, encoding="utf-8")
        return rows, {"source": "live", "fetched_at": None}
    try:
        snap = json.loads((SNAPSHOT_DIR / f"{slug}.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise RuntimeError("live prices are unavailable and there is no saved snapshot for this crop")
    saved = snap["rows"]
    if state:
        saved = [r for r in saved if r["state"].lower() == state.lower()]
    return saved, {"source": "snapshot", "fetched_at": snap["fetched_at"]}


def estimate_route(a: tuple, b: tuple) -> tuple[float, float]:
    """Offline fallback: straight-line distance x 1.3 for road winding, at an average 45 km/h."""
    km = haversine_km(a, b) * 1.3
    return km, km / 45.0


def net_price(modal: float, distance_km: float, drive_hours: float, commodity: str, a: Assumptions) -> tuple:
    """Return (transport, spoilage, fees, net), all Rs per quintal (100 kg)."""
    transport = a.truck_rate_rs_per_tonne_km * distance_km / 10.0  # 1 quintal = 0.1 tonne
    spoil_pct = a.spoilage_pct_per_hour.get(commodity.lower(), a.spoilage_pct_per_hour["default"]) * drive_hours
    spoilage = modal * spoil_pct / 100.0
    fees = modal * (a.market_fee_pct + a.commission_pct) / 100.0
    return transport, spoilage, fees, modal - transport - spoilage - fees
