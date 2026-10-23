# HANDOFF: Fetch-A-Thon 3.0 agent

## Project in one paragraph
Laksh Pradhwani's entry for Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union, Sat 24 Oct 2026, Masters' Union Gurugram, build 10:30 to ~17:50). Build an AI agent registered on Agentverse, speaking the Agent Chat Protocol, discoverable and fully usable inside an ASI:One chat, doing real multi-step tool use. Team ID fetchathon3.0-5865, Laksh is lead. The project idea is **not decided**: Laksh picks it on the day after the 10:15 challenge brief.

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
- `README.md`: public README with the two required badges; agent name/address table to fill in.
- `scripts/handoff.mjs`, `.githooks/pre-commit`, `.claude/settings.json`: HANDOFF.md automation.
- `examples/sun_expert_agent.py`: working ASI:One-compatible chat agent template (ACK, ASI1 call, reply). Copy it to start the real agent.

## Status
- Prep done (23 Oct night): venv + packages (AgentChatProtocol 0.3.0), examples cloned, repo public and pushed.
- ASI:One API key created ("fetchathon laptop") and saved in `.env`; verified with a real call to `asi1`. Random `AGENT_SEED_PHRASE` in `.env`.
- Sun-expert loop verified **locally** (client agent -> agent -> ASI1 -> reply).
- Agentverse API key ("fetchathon laptop 2", scopes hosting + mailbox, expires in 30 days) saved in `.env`; verified (hosting API 200). A first unused key "fetchathon laptop" also exists (its value was lost) and can be revoked at agentverse.ai/profile/api-keys.
- **Mailbox leg verified:** test agent `ASI-agent` address `agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4` registered as a mailbox agent; its Agentverse profile shows Active + "ASI Available". It only works while `examples/sun_expert_agent.py` runs with `USE_MAILBOX=1`.
- NOT yet verified: an actual chat from ASI:One to this agent. ASI:One looked signed out in the automation Chrome (mention search stuck on "Searching..."), so Laksh must sign in to asi1.ai there (or test in his own Chrome at https://asi1.ai/ai/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4).
- Not done: Discord join, teammates agreed, free-month offer (optional: Pro is $100/month and Start Trial goes to billing; free plan includes `asi1`).

## Gotchas learned
- An explicit `endpoint=` on `Agent(...)` overrides `mailbox=True`; the template now sets only one of them.
- The Agentverse Inspector page can't reach `localhost:8001` (Chrome Local Network Access block). Workaround that worked: `POST http://127.0.0.1:8001/connect` with `{"user_token": <Agentverse key>, "agent_type": "mailbox"}`.
- Generating an Agentverse API key triggers a fresh Google/fetch.ai OAuth consent ("Allow Access") and then shows the key once. Copy it via the clipboard, never paste keys into chat or git.
- ASI:One key page is asi1.ai/platform/developer (docs link /dashboard/api-keys 404s). Key names allow only letters, numbers, spaces.

## Next steps (in order)
1. Laksh signs in to asi1.ai, opens the agent chat link above and sends "Give me one short fact about the sun" to confirm the ASI:One leg.
2. Join Discord (channel Fetch-A-Thon 3.0) and agree roles with teammates.
3. On the day: decide the project after the 10:15 brief, build from `examples/sun_expert_agent.py`, submit by 16:30 to 17:50 (GitHub repo, Agentverse profile URL(s), public ASI:One chat URL, 3 to 5 min video, write-up, via Devpost).
4. Stop the test agent when done (it is running in the background on port 8001).

## Open questions / waiting on others
- Who is on the team (email lists only Laksh as lead).
- Devpost link and where to submit.
- Results time: 12:15 (hackpack) vs 10:00 (ASI:One) on 28 Oct.

## Decisions not to undo
- Project idea is chosen by Laksh on the day, not before.
- Repo is public; no secrets ever committed.
- Commit small and push each one (Laksh said yes, 23 Oct 2026).

## Session log (newest first)
- 2026-10-24 (00:30 to 01:10): created Agentverse key into `.env`; fixed template (endpoint vs mailbox); connected mailbox via `/connect`; agent shows Active + ASI Available on Agentverse. ASI:One chat test blocked by signed-out ASI:One in the automation browser.
- 2026-10-24 (just after midnight): created ASI:One key into `.env`, verified; ran Sun-expert example locally end to end; added `examples/sun_expert_agent.py`; fixed the key URL (asi1.ai/platform/developer). Agentverse login still needed.
- 2026-10-23: scaffolded project, Python 3.11 venv, installed uagents/openai/python-dotenv, cloned fetchai/innovation-lab-examples to `C:\dev\fetchathon-ref`, added handoff automation.

<!-- handoff:auto:start -->
## Auto: repo state

_Refreshed 24 Oct 2026, 12:30 am IST by `scripts/handoff.mjs` (runs on every commit). Don't edit inside this block._

Branch: `main` · remote: https://github.com/TheRealLaksh/fetchathon-3-agent.git

### Last 15 commits

- `6a322b4` 2026-10-24 00:01 Fix ASI:One API key URL and update handoff status
- `9638ac5` 2026-10-24 00:01 Add working Sun-expert chat agent template (ASI:One compatible)
- `c8f0006` 2026-10-23 23:56 Add HANDOFF.md and its automation (stop hook, pre-commit refresh)
- `fe9ea20` 2026-10-23 23:56 Add README with required badges, gitignore, env example and requirements

### Uncommitted changes at refresh time

```
M HANDOFF.md
M  examples/sun_expert_agent.py
```
<!-- handoff:auto:end -->
