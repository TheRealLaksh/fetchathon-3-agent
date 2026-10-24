"""Messages the Mandi desk agents send each other (agent-to-agent, not the ASI:One chat protocol)."""
from typing import List, Optional

from uagents import Model


class MandiRow(Model):
    market: str
    district: str
    state: str
    variety: str
    arrival_date: str
    min_price: float  # Rs per quintal
    max_price: float
    modal_price: float


class PriceRequest(Model):
    commodity: str
    states: List[str] = []  # empty = all states
    limit: int = 1000


class PriceReply(Model):
    commodity: str
    rows: List[MandiRow]
    error: Optional[str] = None
    source: str = "live"  # "live", or "snapshot" when the government API was unreachable
    fetched_at: Optional[str] = None  # when the snapshot was saved (snapshot only)


class Place(Model):
    market: str
    district: str
    state: str


class RouteRequest(Model):
    origin: str  # free text, e.g. "Gurugram, Haryana"
    places: List[Place]
    max_radius_km: float = 300.0


class RouteInfo(Model):
    market: str
    district: str
    state: str
    distance_km: float  # real road distance (OSRM)
    drive_hours: float
    approx: bool = False  # True when only the district centre could be located


class RouteReply(Model):
    origin: str
    origin_found: bool
    routes: List[RouteInfo]
    skipped: int = 0  # places we could not locate or that were outside the radius
    estimated: int = 0  # routes estimated from straight-line distance because the routing service was down
    error: Optional[str] = None


class WeatherRequest(Model):
    places: List[str]  # free text, e.g. "Gurugram, Haryana" or "Rohtak, Haryana, India"


class WeatherInfo(Model):
    place: str
    found: bool  # False when the place could not be located or the weather service did not answer
    date: Optional[str] = None
    max_c: Optional[float] = None
    min_c: Optional[float] = None
    rain_chance_pct: Optional[float] = None
    rain_mm: Optional[float] = None


class WeatherReply(Model):
    items: List[WeatherInfo]
    source: str = "Open-Meteo"
    error: Optional[str] = None
