"""Pre-warm the geocode cache so the first real question is fast (Nominatim allows 1 request/second).

Run when the agents are NOT answering questions (two processes writing the cache at once can lose entries):
    python -m mandi.warm_cache Tomato Onion Potato -- "Gurugram, Haryana" "Delhi, NCT of Delhi"
Origin state is taken as the text after the last comma, so write origins as "City, State".
"""
import sys

from dotenv import load_dotenv

from mandi.core import fetch_prices
from mandi.front_agent import MAX_MARKETS
from mandi.logistics_agent import compute
from mandi.models import Place, RouteRequest
from mandi.ranking import search_states

load_dotenv()


def warm(commodity: str, origin: str) -> None:
    state = origin.rsplit(",", 1)[-1].strip()
    wanted = {s.lower() for s in search_states(state)}
    rows = [r for r in fetch_prices(commodity, None, 500) if not wanted or r["state"].lower() in wanted]
    seen, places = set(), []
    for r in rows:  # same selection the front agent makes: unique markets in data order, capped
        key = (r["market"], r["district"], r["state"])
        if key not in seen:
            seen.add(key)
            places.append(Place(market=r["market"], district=r["district"], state=r["state"]))
    reply = compute(RouteRequest(origin=origin, places=places[:MAX_MARKETS]))
    print(f"{commodity} from {origin}: {len(reply.routes)} routed, {reply.skipped} skipped", flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    split = args.index("--") if "--" in args else len(args)
    crops, origins = args[:split], args[split + 1 :] or ["Gurugram, Haryana"]
    for crop in crops:
        for origin in origins:
            warm(crop, origin)
