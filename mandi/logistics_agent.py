"""Logistics agent: answers RouteRequest with real road distance and drive time (OSM + OSRM)."""
import asyncio
import os
import re

from dotenv import load_dotenv
from uagents import Agent, Context

from mandi.core import estimate_route, geocode, haversine_km, road_route
from mandi.models import RouteInfo, RouteReply, RouteRequest

load_dotenv()


def _clean(name: str) -> str:
    """Strip words that stop OpenStreetMap matching: APMC, Mandi, brackets, stray commas."""
    name = re.sub(r"\(.*?\)|\b(?:APMC|Mandi|Market|New Grain)\b|,", " ", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip()


def _locate(place) -> tuple[tuple | None, bool]:
    """(position, approx). Market name first; falls back to the district centre (approx=True)."""
    clean = _clean(place.market)
    if clean:
        pos = geocode(f"{clean}, {place.district}, {place.state}, India")
        if pos:
            return pos, False
    pos = geocode(f"{place.district}, {place.state}, India")
    return pos, True


def compute(req: RouteRequest) -> RouteReply:
    origin = geocode(req.origin)
    if not origin:
        return RouteReply(origin=req.origin, origin_found=False, routes=[], error="Could not locate the origin")
    routes, skipped, estimated = [], 0, 0
    for p in req.places:
        pos, approx = _locate(p)
        if not pos or haversine_km(origin, pos) > req.max_radius_km:
            skipped += 1
            continue
        try:
            leg = road_route(origin, pos)
        except Exception:  # routing service unreachable: estimate instead of failing the whole answer
            leg = estimate_route(origin, pos)
            approx = True
            estimated += 1
        if not leg:
            skipped += 1
            continue
        routes.append(
            RouteInfo(market=p.market, district=p.district, state=p.state, distance_km=leg[0], drive_hours=leg[1],
                      approx=approx)
        )
    return RouteReply(origin=req.origin, origin_found=True, routes=routes, skipped=skipped, estimated=estimated)


def make_logistics_agent(port: int = 8003, **kwargs) -> Agent:
    agent = Agent(name="mandi-logistics-agent", seed=os.environ["AGENT_SEED_PHRASE"] + "-logistics", port=port, **kwargs)

    @agent.on_message(RouteRequest, replies=RouteReply)
    async def handle(ctx: Context, sender: str, msg: RouteRequest):
        try:
            reply = await asyncio.to_thread(compute, msg)
        except Exception as err:
            ctx.logger.exception("routing failed")
            reply = RouteReply(origin=msg.origin, origin_found=False, routes=[], error=str(err)[:200])
        await ctx.send(sender, reply)

    return agent


if __name__ == "__main__":
    make_logistics_agent(endpoint=["http://127.0.0.1:8003/submit"]).run()
