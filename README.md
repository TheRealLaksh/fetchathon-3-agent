![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

# Mandi Net-Price Desk

![Mandi Net-Price Desk](assets/banner.png)

An ASI:One agent that tells an Indian produce trader **which mandi to sell at, or buy from, today**, ranked by what they actually clear after real road freight, spoilage and fees. The sticker price at a mandi is not the answer: a mandi that pays Rs 100 more per quintal can lose once you drive another 200 km.

Built at Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union Gurugram, 24 Oct 2026), the "ASI:One Agent Challenge: From Intent to Action". Team ID `fetchathon3.0-5865`.

**Team:** Laksh Pradhwani (lead), Mark Patel, Aryan Rao, Saiansh Kathuria.

## Try it in ASI:One

Open the agent in ASI:One and ask in plain language:

- Profile: https://asi1.ai/ai/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4
- Handle: `@mandi-desk`

> I have 25 tonnes of tomato in Gurugram. Where should I sell today?

> I run a restaurant in Delhi. Where is onion cheapest to buy today?

Replies take a while: ASI:One passes the message to the agent through the Agentverse mailbox (about 1 to 2 minutes), and the agent then pulls live data. The chat page may need a reload to show the reply.

## Agents

| Agent | Address | Agentverse profile | What it does |
|---|---|---|---|
| **Mandi Net-Price Desk** (front agent, `@mandi-desk`) | `agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4` | [profile](https://agentverse.ai/agents/details/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4/profile) | Speaks the Agent Chat Protocol, reads the request with the ASI1 LLM, calls the two agents below, ranks the mandis, replies in chat with a table and an interactive card. |
| Mandi Price Agent | `agent1qdppp6kky9mlmq9j4c7v0nksqpvusy7w9vjxylzuu6xt48fs20mw7ecwcp0` | [profile](https://agentverse.ai/agents/details/agent1qdppp6kky9mlmq9j4c7v0nksqpvusy7w9vjxylzuu6xt48fs20mw7ecwcp0/profile) | Fetches today's real modal prices per mandi from the government daily mandi dataset (data.gov.in). Falls back to the last saved snapshot if the API is down. |
| Mandi Logistics Agent | `agent1qtw0yw8kanxv48wd0v2zrhdg4p6ewersauhstygfy4s2qv20fyxkjl8w9y3` | [profile](https://agentverse.ai/agents/details/agent1qtw0yw8kanxv48wd0v2zrhdg4p6ewersauhstygfy4s2qv20fyxkjl8w9y3/profile) | Locates each mandi (OpenStreetMap) and returns real road distance and drive time (OSRM). Estimates from straight-line distance if the routing service is down. |

The front agent is a mailbox agent (reachable from ASI:One). The two helper agents run as local agents registered on Agentverse (their profile pages show Active and Local) and are called by the front agent over HTTP. The three are separate uAgents that exchange typed messages (`mandi/models.py`), so this is a real multi-agent workflow, not one agent calling functions.

## What it answers (real run, 24 Oct 2026)

Question: *I have 8 tonnes of tomato in Gurugram. Where should I sell today?*

| # | Mandi | Price Rs/qtl | Road km | Drive h | You actually clear Rs/qtl |
|---|---|---|---|---|---|
| 1 | Sohna APMC (Gurgaon, Haryana) | 2,500 | 18 | 0.3 | **2,443** |
| 2 | Gohana APMC (Sonipat, Haryana) | 2,500 | 102 | 1.4 | **2,411** |
| 3 | Narnaul APMC (Mahendragarh-Narnaul, Haryana) | 2,500 | 113 | 1.4 | **2,407** |
| 4 | Patiala APMC (Patiala, Punjab) | 2,400 | 261 | 3.3 | **2,254** |
| 5 | Dhand APMC (Kaithal, Haryana) | 2,150 | 189 | 2.4 | **2,038** |
| 6 | Machhiwara APMC (Ludhiana, Punjab) | 2,200 | 323 | 4.2 | **2,036** |

Net price = modal price minus transport minus transit loss minus mandi fees, per quintal. Buyer mode ranks by landed cost instead. Distances marked `~` are approximate (only the district centre could be located). The reply always lists the assumptions it used.

## How it works

```
ASI:One chat  ->  Agentverse mailbox  ->  Mandi Net-Price Desk (front agent)
                                              |-- ASI1 LLM: crop, place, sell or buy, quantity
                                              |-- Price Agent     -> data.gov.in daily mandi prices
                                              |-- Logistics Agent -> OpenStreetMap + OSRM road routes
                                              |-- ranking (mandi/ranking.py) and load plan (mandi/extras.py)
                                              `-> text table + interactive card back to ASI:One
```

Fetch.ai pieces used: uAgents, Agentverse mailbox agent, Agent Chat Protocol, ASI1 LLM, agent-to-agent messages, ASI:One interactive card.

## Real data, and what is an assumption

- **Real:** mandi prices (data.gov.in, dated the day of the question), mandi locations (OpenStreetMap), road distance and drive time (OSRM).
- **Assumptions** (shown in every reply, and the user can override them in chat, for example "my truck costs Rs 4 per tonne-km"): freight Rs 3.0 per tonne-km, market fee 2%, agent commission 0% (not included), transit loss 0.15 to 0.25% of value per drive hour. Sources and how each was derived are in [SOURCES.md](SOURCES.md). The top of the ranking did not change in our sensitivity tests, but the net figures move with these numbers.

## Run it

Needs Python 3.10 to 3.13 (3.14 is not supported by uAgents yet).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in ASI1_API_KEY, AGENTVERSE_API_KEY, DATA_GOV_IN_API_KEY and a long AGENT_SEED_PHRASE
```

Start three processes (each in its own terminal), the front agent last:

```bash
python -m mandi.price_agent
python -m mandi.logistics_agent
USE_MAILBOX=1 python -m mandi.front_agent     # then connect the mailbox from the Inspector link it prints
```

Local test without ASI:One: `python -m mandi.chat_test "I have 8 tonnes of tomato in Gurugram. Where should I sell today?"`

Other tools: `python -m mandi.selftest` (9 offline tests), `python -m mandi.warm_cache Tomato Onion Potato -- "Gurugram, Haryana" "Delhi, NCT of Delhi"` (pre-loads map lookups; the first question about a new crop or town is slow without it).

## Known limits

- The agents run on a laptop; the mailbox agent only answers while all three processes are running.
- First question for a crop or town not yet cached can take minutes (the free map lookup allows one request per second).
- The government dataset holds only today's prices, so there is no trend or "wait and sell later" advice.
- Agent commission is not included unless the user states it. Freight is derived from long-haul rates; short hauls usually cost more per tonne-km.
- The interactive card renders in ASI:One. The "Plan this load" button flow was verified locally and in unit tests but not confirmed end to end inside ASI:One; typing "plan the load for <mandi>" is also handled.
- Some mandis could only be located by district, so their distance is approximate and marked `~`.

## Repository

```
mandi/core.py            data calls, net-price maths, snapshots, fallbacks
mandi/models.py          messages between the agents
mandi/price_agent.py     Price Agent
mandi/logistics_agent.py Logistics Agent
mandi/front_agent.py     ASI:One-facing agent
mandi/ranking.py         ranking and reply text
mandi/extras.py          interactive card and load planner
mandi/selftest.py        offline tests
SOURCES.md               sources for the assumptions
docs/                    write-up and video script
assets/                  profile picture and banner
```

## Extra resources

- ASI:One API key: https://asi1.ai/platform/developer
- Agentverse API key: https://agentverse.ai/profile/api-keys
- Docs: https://innovationlab.fetch.ai/resources/docs/intro
