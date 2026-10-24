"""Weather agent: answers WeatherRequest with today's real weather (Open-Meteo) for the origin and the top mandis."""
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from uagents import Agent, Context

from mandi.branding import profile_kwargs
from mandi.core import geocode, weather_today
from mandi.models import WeatherInfo, WeatherReply, WeatherRequest

load_dotenv()


def compute(req: WeatherRequest) -> WeatherReply:
    places = req.places[:6]  # the front agent asks for three; keep the free service's load small
    positions = [geocode(q) for q in places]  # sequential and cached (Nominatim allows 1 request/second)
    with ThreadPoolExecutor(max_workers=4) as pool:
        weather = list(pool.map(lambda pos: weather_today(*pos) if pos else None, positions))
    items = [
        WeatherInfo(place=q, found=w is not None, **(w or {}))
        for q, w in zip(places, weather)
    ]
    return WeatherReply(items=items)


def make_weather_agent(port: int = 8004, **kwargs) -> Agent:
    agent = Agent(
        name="Mandi Weather Agent", seed=os.environ["AGENT_SEED_PHRASE"] + "-weather", port=port,
        **profile_kwargs(
            "agent-readme-weather.md",
            "Returns today's real weather (max and min temperature, rain chance) for a trader's place and the top "
            "mandis, from Open-Meteo. Part of Mandi Net-Price Desk.",
        ),
        **kwargs,
    )

    @agent.on_message(WeatherRequest, replies=WeatherReply)
    async def handle(ctx: Context, sender: str, msg: WeatherRequest):
        try:
            reply = await asyncio.to_thread(compute, msg)
        except Exception as err:  # the desk keeps answering without weather
            ctx.logger.exception("weather lookup failed")
            reply = WeatherReply(items=[], error=str(err)[:200])
        await ctx.send(sender, reply)

    return agent


if __name__ == "__main__":
    make_weather_agent(endpoint=["http://127.0.0.1:8004/submit"]).run()
