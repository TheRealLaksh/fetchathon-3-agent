"""Price agent: answers PriceRequest with today's real mandi rows from data.gov.in."""
import asyncio
import os

from dotenv import load_dotenv
from uagents import Agent, Context

from mandi.branding import profile_kwargs
from mandi.core import fetch_prices_with_source
from mandi.models import MandiRow, PriceReply, PriceRequest

load_dotenv()


def make_price_agent(port: int = 8002, **kwargs) -> Agent:
    agent = Agent(
        name="Mandi Price Agent", seed=os.environ["AGENT_SEED_PHRASE"] + "-price", port=port,
        **profile_kwargs(
            "agent-readme-price.md",
            "Fetches today's real modal mandi prices per market from the government daily mandi dataset "
            "(data.gov.in). Part of Mandi Net-Price Desk.",
        ),
        **kwargs,
    )

    @agent.on_message(PriceRequest, replies=PriceReply)
    async def handle(ctx: Context, sender: str, msg: PriceRequest):
        try:
            rows, info = await asyncio.to_thread(fetch_prices_with_source, msg.commodity, None, msg.limit)
            wanted = {s.lower() for s in msg.states}
            out = []
            for r in rows:
                if wanted and r["state"].lower() not in wanted:
                    continue
                try:
                    out.append(
                        MandiRow(
                            market=r["market"], district=r["district"], state=r["state"], variety=r["variety"],
                            arrival_date=r["arrival_date"], min_price=float(r["min_price"]),
                            max_price=float(r["max_price"]), modal_price=float(r["modal_price"]),
                        )
                    )
                except (KeyError, ValueError, TypeError):
                    continue  # skip rows with missing or non-numeric prices
            await ctx.send(sender, PriceReply(commodity=msg.commodity, rows=out, source=info["source"],
                                              fetched_at=info["fetched_at"]))
        except Exception as err:  # keep the desk alive; the front agent reports the error
            ctx.logger.exception("price lookup failed")
            await ctx.send(sender, PriceReply(commodity=msg.commodity, rows=[], error=str(err)[:200]))

    return agent


if __name__ == "__main__":
    make_price_agent(endpoint=["http://127.0.0.1:8002/submit"]).run()
