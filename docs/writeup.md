# Mandi Net-Price Desk: write-up

**Tagline:** Which mandi should you sell at today? Ranked by what you actually clear, not the sticker price.

## The problem

A produce trader in Gurugram with a truckload of tomatoes can sell at dozens of mandis across Haryana, Rajasthan, Punjab and beyond. The government publishes today's price at each one, but the highest price is rarely the best deal. The trader still pays for the drive, loses some produce on the road, and pays mandi fees. Working that out for every mandi means a spreadsheet, a distance lookup per market, and a freight guess, so most people sell at the mandi they always use.

Buyers have the mirror problem: a restaurant or hotel kitchen wants the cheapest landed cost for onion or potato, not the cheapest sticker price.

## What it does

You write one sentence in ASI:One, for example *"I have 25 tonnes of tomato in Gurugram. Where should I sell today?"*. The agent:

1. Understands the crop, the place, whether you are selling or buying, and the quantity.
2. Pulls today's real mandi prices from the government dataset.
3. Finds real road distance and drive time to each candidate mandi.
4. Subtracts transport, transit loss and mandi fees, and ranks the mandis by **net rupees per quintal** (buyers get landed cost instead).
5. Replies with a ranked table, the recommendation, the money difference for your quantity, and every assumption it used. An interactive card lists the top mandis, and a load plan turns the answer into trucks and totals.

Real example from 24 Oct 2026 (tomato, from Gurugram): Sohna, Gohana and Narnaul all paid Rs 2,500 per quintal, but the net figures were Rs 2,443, 2,411 and 2,407 because of distance. Patiala paid Rs 2,400 and netted Rs 2,254. For 80 quintals, the best choice over the last one shown was worth about Rs 32,500.

## Who it is for

- Traders and farmer producer organisations deciding where to send a load.
- Restaurants, hotels and wholesalers sourcing fruit and vegetables.
- Anyone who has to choose between nearby markets with different prices.

## How we built it

Four separate uAgents that exchange typed messages:

- **Mandi Net-Price Desk** (front agent, mailbox agent on Agentverse, Agent Chat Protocol). It uses the ASI1 LLM only to read the request, then orchestrates the others, ranks the results and replies.
- **Price Agent**, which calls the data.gov.in daily mandi dataset.
- **Logistics Agent**, which geocodes mandis with OpenStreetMap and gets road distance and drive time from OSRM.
- **Weather Agent**, which returns today's real weather (temperature and rain chance, Open-Meteo) for the trader's place and the top mandis; shown next to the ranking, it does not change the maths.

The ranking maths is deterministic code, not LLM output, so the numbers are repeatable and checked by 9 offline tests.

Personal and multilingual: the desk remembers each user's crop, place and cost settings (per chat, clearable with "forget me"), accepts follow-ups such as "what if 60 quintals", and understands Hindi and Hinglish. The ASI1 model also writes a two-sentence "why this one" explanation, but only from the ranking numbers: any sentence with a number the data does not contain, or any timing advice, is discarded. Route lookups are cached and run in parallel, so the agents' own work now typically takes well under half a minute (it was about a minute before), on top of ASI:One's message delay (extra offline tests: `python -m mandi.test_upgrades`). Fetch.ai pieces used: uAgents, Agentverse mailbox, Agent Chat Protocol, ASI1 LLM, agent-to-agent messaging, and an ASI:One interactive card.

## What makes it dependable

- **Real data, labelled assumptions.** Prices, locations and distances are live. The three cost assumptions (freight, mandi fee, transit loss) are shown in every reply, are sourced in `SOURCES.md`, and the user can override them in chat ("my truck costs Rs 4 per tonne-km").
- **Honest about what it does not know.** Agent commission is excluded unless the user states it. Mandis located only by district are marked as approximate. Dated prices are shown.
- **Fallbacks.** If the government API is unreachable, the agent answers from the last saved snapshot and says so. If the routing service is down, it estimates distance from straight-line distance and marks it approximate. We tested the price fallback live by giving the agent a wrong API key.
- **Stress-tested ranking.** The top of the ranking did not change when we pushed freight to Rs 5 per tonne-km, transit loss to 0.5% an hour, or fees plus commission to 8%.

## Challenges

- The free map lookup allows one request per second, so a cold first question is slow. We added a cache and a warm-up script.
- Mandi names in the dataset do not always match map names ("Barwala(Hisar) APMC"), so we clean them and fall back to the district centre, marked approximate.
- Failed lookups were first cached as "not found", which hid real mandis. We fixed it to cache only real answers.
- The dataset has no price history, so we did not build a "sell now or wait" feature rather than invent a trend.

## What we are proud of

A working multi-agent workflow that answers a real money question using live government data, with the assumptions on the table and fallbacks for when a data source fails.

## What we know is unfinished

- The agents run on a laptop; the mailbox agent only answers while they are running.
- ASI:One takes 1 to 2 minutes to pass a message to the agent and needs a page reload to show the reply.
- The interactive card renders in ASI:One and the "Plan this load" button was tested end to end there on 25 Oct 2026 (the plan came back, after about 6 minutes of mailbox delay that time).
- Freight comes from long-haul rates; short hauls usually cost more per tonne-km.

## What is next

- Add agent commission and a per-state fee table.
- Keep daily snapshots so a price trend and "wait or sell" advice become possible.
- Host the agents on Agentverse so they do not depend on a laptop.
- Payment Protocol for paid, premium lookups.

## Built with

Python, uAgents, Agentverse, ASI:One and the ASI1 API, data.gov.in (daily mandi prices), OpenStreetMap Nominatim, OSRM.

## Links

- Repo: https://github.com/TheRealLaksh/fetchathon-3-agent
- Agent in ASI:One: https://asi1.ai/ai/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4 (handle `@mandi-desk`)
- Agentverse profile: https://agentverse.ai/agents/details/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4/profile
- Public ASI:One chat: _paste the shared chat link here_
- Demo video: _paste the video link here_
