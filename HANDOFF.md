# HANDOFF: Fetch-A-Thon 3.0 agent

## Project in one paragraph
Laksh Pradhwani's entry for Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union, Sat 24 Oct 2026, Masters' Union Gurugram, build 10:30 to ~17:50). Build an AI agent registered on Agentverse, speaking the Agent Chat Protocol, discoverable and fully usable inside an ASI:One chat, doing real multi-step tool use. Team ID fetchathon3.0-5865, Laksh is lead. **Project chosen 24 Oct 2026 (~14:00): Mandi Net-Price Desk** (Laksh picked it himself from 3 options): an ASI:One multi-agent desk that ranks mandis by NET rupees per quintal (live data.gov.in price minus real OSRM transport, spoilage and fees).

## Links
- Local path: `C:\dev\fetchathon-3` · reference examples (read-only clone): `C:\dev\fetchathon-ref`
- Repo: https://github.com/TheRealLaksh/fetchathon-3-agent (public)
- Vault notes: `C:\Users\laksh\OneDrive\Documents\Obsidian Vault\05 Resources\Fetch-A-Thon 3.0\` (brief, hackpack, all docs)
- Hackpack: https://innovationlab.fetch.ai/events/hackathons/fetch-a-thon-3/hackpack
- ASI:One event page: https://asi1.ai/events/4f64e97b-656c-42bb-aa09-59449c2a5fad
- Keys: ASI:One https://asi1.ai/platform/developer (the docs' /dashboard/api-keys link 404s) · Agentverse https://agentverse.ai/profile/api-keys (values only in `.env`)

## Stack and how to run
Python 3.11 venv (`.venv`), `uagents>=0.25.5`, `openai` (ASI1 is OpenAI-compatible at `https://api.asi1.ai/v1`, model `asi1`), `python-dotenv`.
```
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # fill in keys + a long random AGENT_SEED_PHRASE
python <agent>.py
```
Mailbox agent: open the Inspector link it prints, Connect, Mailbox, then "Chat with Agent" in ASI:One. A mailbox agent only works while the script runs.

## Code map
- `mandi/warm_cache.py`: pre-warms the geocode cache. Run when agents are idle: `python -m mandi.warm_cache Tomato Onion Potato -- "Gurugram, Haryana" "Delhi, NCT of Delhi"` (cold first query for a new crop takes minutes).
- `mandi/front_agent.py` (port 8001, ASI:One chat protocol, same seed as the earlier test agent so the existing mailbox works), `mandi/ranking.py` (net-price ranking + reply text + neighbour-state map), `mandi/chat_test.py` (chat client for local tests: `python -m mandi.chat_test "question"`). Full local chain tested 24 Oct: real tomato prices + real routes -> ranked table (Sohna 18 km best, Rs 2,443/qtl net).
- `mandi/models.py`, `mandi/price_agent.py` (port 8002), `mandi/logistics_agent.py` (port 8003): the two real uAgents (agent-to-agent messages). Run each with `python -m mandi.price_agent` etc.; `python -m mandi.local_test` is a client that exercises both. TESTED 24 Oct: 23 real Haryana tomato rows, real road distances from Gurugram (Faridabad 37.8 km, Narnaul 111.6 km).
- `mandi/core.py`: Mandi desk maths + data calls (data.gov.in prices, Nominatim geocode, OSRM route, `net_price`). Keyless parts tested live 24 Oct. Assumptions (truck rate, spoilage, commission) are labelled placeholders.
- `README.md`: public README with the two required badges; agent name/address table to fill in.
- `scripts/handoff.mjs`, `.githooks/pre-commit`, `.claude/settings.json`: HANDOFF.md automation.
- `examples/sun_expert_agent.py`: working ASI:One-compatible chat agent template (ACK, ASI1 call, reply). Copy it to start the real agent.

## Status
- Prep done (23 Oct night): venv + packages (AgentChatProtocol 0.3.0), examples cloned, repo public and pushed.
- ASI:One API key created ("fetchathon laptop") and saved in `.env`; verified with a real call to `asi1`. Random `AGENT_SEED_PHRASE` in `.env`.
- Sun-expert loop verified **locally** (client agent -> agent -> ASI1 -> reply).
- Agentverse API key ("fetchathon laptop 2", scopes hosting + mailbox, expires in 30 days) saved in `.env`; verified (hosting API 200). A first unused key "fetchathon laptop" also exists (its value was lost) and can be revoked at agentverse.ai/profile/api-keys.
- **Mailbox leg verified:** test agent `ASI-agent` address `agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4` registered as a mailbox agent; its Agentverse profile shows Active + "ASI Available". It only works while `examples/sun_expert_agent.py` runs with `USE_MAILBOX=1`.
- **Full pipeline verified (24 Oct 2026, 12:51 AM, by Laksh in his own browser):** in ASI:One he sent `@agent1qv7j... Give me one short fact about the sun` and `ASI-agent` replied (light from the Sun takes about 8 min 20 s to reach Earth). So: ASI:One -> Agentverse mailbox -> local agent -> ASI1 LLM -> reply works. (The automation Chrome showed ASI:One signed out, so the test was done by hand.) Test agent is stopped; restart with `$env:USE_MAILBOX="1"; .venv\Scripts\python.exe examples\sun_expert_agent.py`.
- Not done: Discord join, teammates agreed, free-month offer (optional: Pro is $100/month and Start Trial goes to billing; free plan includes `asi1`).

## Gotchas learned
- An explicit `endpoint=` on `Agent(...)` overrides `mailbox=True`; the template now sets only one of them.
- The Agentverse Inspector page can't reach `localhost:8001` (Chrome Local Network Access block). Workaround that worked: `POST http://127.0.0.1:8001/connect` with `{"user_token": <Agentverse key>, "agent_type": "mailbox"}`.
- Generating an Agentverse API key triggers a fresh Google/fetch.ai OAuth consent ("Allow Access") and then shows the key once. Copy it via the clipboard, never paste keys into chat or git.
- ASI:One key page is asi1.ai/platform/developer (docs link /dashboard/api-keys 404s). Key names allow only letters, numbers, spaces.

## Next steps (in order)
00. Agentverse profile: rename to Mandi Net-Price Desk + README/description; test buyer mode and other crops (onion, potato); tune Assumptions with real numbers; maybe Interactive Card; freeze 15:30; shared ASI:One chat URL; video; Devpost.
0. MANDI DESK: data.gov.in key is in .env (done 24 Oct). Verified fresh rows dated 24/10/2026 for Tomato, Onion, Potato, Banana, Cauliflower (Tamil Nadu has most rows; Haryana/Punjab 12-24 each; Apple timed out once). Fields: arrival_date, commodity, district, grade, market, max_price, min_price, modal_price, state, variety. Next: front ASI:One agent (chat protocol) that calls both agents + net-price card + advisor; then build Price agent + Logistics agent as real uAgents, front agent on ASI:One, card output; freeze 15:30. Fallback if data fails: landed-cost desk (Frankfurter FX verified).
1. Join Discord (channel Fetch-A-Thon 3.0) and agree roles with teammates.
2. On the day: decide the project after the 10:15 brief, build from `examples/sun_expert_agent.py`, submit by 16:30 to 17:50 (GitHub repo, Agentverse profile URL(s), public ASI:One chat URL, 3 to 5 min video, write-up, via Devpost).
3. Add the real agent's name/address to the README table; keep the two badges.

## Open questions / waiting on others
- Who is on the team (email lists only Laksh as lead).
- Devpost link and where to submit.
- Results time: 12:15 (hackpack) vs 10:00 (ASI:One) on 28 Oct.

## Decisions not to undo
- Project idea is chosen by Laksh on the day, not before.
- Repo is public; no secrets ever committed.
- Commit small and push each one (Laksh said yes, 23 Oct 2026).

## Session log (newest first)
- 2026-10-24 (~16:15): assumptions now sourced (SOURCES.md): freight Rs 3.0/tonne-km, market fee 2% (Haryana 1%+1% RDF), agent commission 0% (not included, no reliable rate), transit loss 0.25/0.15/0.2 %/h (tomato/onion/other, derived from NABCONS 2022). Users can override in chat (truck rate, commission, market fee). Ranking order is insensitive to these (tested). Front agent restarted with mailbox on the new code. Unverified at primary source: NABCONS crop-by-stage tables, current Haryana commission schedule.
- 2026-10-24 (~15:50): ran warm_cache for Tomato/Onion/Potato from Gurugram + Delhi (117 cache entries; file is gitignored, lives only on this laptop). A warm tomato question now answers in ~30 s including the test client start-up (was minutes cold). Potato, off-topic and onion buy/sell tests all passed.
- 2026-10-24 (~15:35): Agentverse starter prompts added; onion (sell) test OK but took minutes on a cold cache; added warm_cache.py. Potato + off-topic tests were still running.
- 2026-10-24 (~15:20): Agentverse profile set (name Mandi Net-Price Desk, 160-char description, README); buyer mode tested OK (onion, Delhi); reply wording fixed. KNOWN RISK: a cold geocode cache makes the first query for a new crop/area take minutes (Nominatim 1 req/s) -> PRE-WARM the cache before the demo and before judging.
- 2026-10-24 (~14:55): END-TO-END IN ASI:ONE WORKS. Question sent from Laksh's ASI:One (profile chat of agent1qv7j...) -> mailbox -> front agent -> Price + Logistics agents -> ranked table with Sohna APMC best (Rs 2,443/qtl net). Needs all three processes running on the laptop (price, logistics, front with USE_MAILBOX=1). ASI:One still shows the old profile name 'ASI-agent': set name/description on the Agentverse agent profile. Nothing else changed in code.
- 2026-10-24 (~14:50): built front agent (LLM intent extraction, calls Price + Logistics agents, ranks, replies); fixed geocode caching of failed lookups (only cache real answers) and the market-name cleaner; district-centre fallbacks are shown with ~. Gotcha: writing regex with backslash-b through a bash heredoc turned it into a backspace char; write it via a file using chr(92).
- 2026-10-24 (~15:00): built and tested Price + Logistics agents as separate processes (client test passes). Gotchas: Bureau did not fire handlers here, use separate processes with explicit endpoint; agent ctx.storage persists across runs (use in-memory flags in tests); python -u needed for logs when redirecting.
- 2026-10-24 (~14:30): generated data.gov.in key in Laksh's logged-in Chrome (copied via clipboard to .env, never printed); confirmed fresh mandi rows for 5 crops; added retry to fetch_prices.
- 2026-10-24 (~14:00): project locked (Mandi Net-Price Desk); added mandi/core.py (geocode, OSRM route, net-price maths) tested live without the data key.
- 2026-10-24 (~01:00): Laksh confirmed the ASI:One -> agent chat works (screenshot); stopped the test agent; handoff updated.
- 2026-10-24 (00:30 to 01:10): created Agentverse key into `.env`; fixed template (endpoint vs mailbox); connected mailbox via `/connect`; agent shows Active + ASI Available on Agentverse. ASI:One chat test blocked by signed-out ASI:One in the automation browser.
- 2026-10-24 (just after midnight): created ASI:One key into `.env`, verified; ran Sun-expert example locally end to end; added `examples/sun_expert_agent.py`; fixed the key URL (asi1.ai/platform/developer). Agentverse login still needed.
- 2026-10-23: scaffolded project, Python 3.11 venv, installed uagents/openai/python-dotenv, cloned fetchai/innovation-lab-examples to `C:\dev\fetchathon-ref`, added handoff automation.

<!-- handoff:auto:start -->
## Auto: repo state

_Refreshed 24 Oct 2026, 3:07 pm IST by `scripts/handoff.mjs` (runs on every commit). Don't edit inside this block._

Branch: `main` · remote: https://github.com/TheRealLaksh/fetchathon-3-agent.git

### Last 15 commits

- `9d98aeb` 2026-10-24 15:02 Record cache warm-up and test results
- `ff9211f` 2026-10-24 14:57 Add geocode cache warm-up script
- `14869f9` 2026-10-24 14:55 Fix reply wording for buyer mode and plural; record profile setup
- `8a9ab14` 2026-10-24 14:52 Record end-to-end ASI:One success in handoff
- `5551520` 2026-10-24 14:49 Add front ASI:One agent, net-price ranking and chat test; fix geocode caching
- `9dae140` 2026-10-24 14:31 Add Price and Logistics agents with local end-to-end test
- `70468d9` 2026-10-24 14:21 Retry mandi price fetch on timeout; record verified fresh data
- `0b87896` 2026-10-24 14:04 Add Mandi Net-Price Desk core: geocode, OSRM route, net-price maths
- `70cca5b` 2026-10-24 00:52 Handoff: ASI:One chat leg verified end to end, test agent stopped
- `a922855` 2026-10-24 00:30 Fix template: endpoint overrides mailbox, set only one
- `6a322b4` 2026-10-24 00:01 Fix ASI:One API key URL and update handoff status
- `9638ac5` 2026-10-24 00:01 Add working Sun-expert chat agent template (ASI:One compatible)
- `c8f0006` 2026-10-23 23:56 Add HANDOFF.md and its automation (stop hook, pre-commit refresh)
- `fe9ea20` 2026-10-23 23:56 Add README with required badges, gitignore, env example and requirements

### Uncommitted changes at refresh time

```
M  HANDOFF.md
A  SOURCES.md
M  mandi/core.py
M  mandi/front_agent.py
M  mandi/ranking.py
```
<!-- handoff:auto:end -->
