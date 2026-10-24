"""Local end-to-end test of the Price and Logistics agents as separate processes.

Start them first (two terminals, or background):
    python -m mandi.price_agent
    python -m mandi.logistics_agent
Then run:  python -m mandi.local_test
A client agent asks the Price agent for tomato rows in Haryana, then asks the Logistics agent
for real road distances from Gurugram to the first few markets, and prints both replies.
"""
import os

from dotenv import load_dotenv
from uagents import Agent, Context
from uagents.crypto import Identity

from mandi.models import Place, PriceReply, PriceRequest, RouteReply, RouteRequest

load_dotenv()
SEED = os.environ["AGENT_SEED_PHRASE"]
PRICE = Identity.from_seed(SEED + "-price", 0).address
LOGISTICS = Identity.from_seed(SEED + "-logistics", 0).address

_asked: list = []  # in-memory, so every run asks once
client = Agent(name="mandi-test-client", seed=SEED + "-client", port=8004, endpoint=["http://127.0.0.1:8004/submit"])


@client.on_interval(period=3.0)
async def ask_prices(ctx: Context):
    if _asked:
        return
    _asked.append(True)
    print("send status:", await ctx.send(PRICE, PriceRequest(commodity="Tomato", states=["Haryana"])), flush=True)


@client.on_message(PriceReply)
async def got_prices(ctx: Context, sender: str, msg: PriceReply):
    print(f"\nPRICE REPLY: {len(msg.rows)} rows, error={msg.error}", flush=True)
    for r in msg.rows[:5]:
        print(f"  {r.market} ({r.district}) modal Rs {r.modal_price}/qtl on {r.arrival_date}", flush=True)
    places = [Place(market=r.market, district=r.district, state=r.state) for r in msg.rows[:5]]
    await ctx.send(LOGISTICS, RouteRequest(origin="Gurugram, Haryana", places=places))


@client.on_message(RouteReply)
async def got_routes(ctx: Context, sender: str, msg: RouteReply):
    print(f"\nROUTE REPLY: origin_found={msg.origin_found}, skipped={msg.skipped}, error={msg.error}", flush=True)
    for r in msg.routes:
        print(f"  {r.market}: {r.distance_km:.1f} km, {r.drive_hours:.2f} h", flush=True)
    os._exit(0)


if __name__ == "__main__":
    client.run()
