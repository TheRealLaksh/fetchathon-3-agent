# HANDOFF: Fetch-A-Thon 3.0 agent

## Project in one paragraph
Laksh Pradhwani's entry for Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union, Sat 24 Oct 2026, Masters' Union Gurugram, build 10:30 to ~17:50). Build an AI agent registered on Agentverse, speaking the Agent Chat Protocol, discoverable and fully usable inside an ASI:One chat, doing real multi-step tool use. Team ID fetchathon3.0-5865, Laksh is lead. The project idea is **not decided**: Laksh picks it on the day after the 10:15 challenge brief.

## Links
- Local path: `C:\dev\fetchathon-3` · reference examples (read-only clone): `C:\dev\fetchathon-ref`
- Repo: https://github.com/TheRealLaksh/fetchathon-3-agent (public)
- Vault notes: `C:\Users\laksh\OneDrive\Documents\Obsidian Vault\05 Resources\Fetch-A-Thon 3.0\` (brief, hackpack, all docs)
- Hackpack: https://innovationlab.fetch.ai/events/hackathons/fetch-a-thon-3/hackpack
- ASI:One event page: https://asi1.ai/events/4f64e97b-656c-42bb-aa09-59449c2a5fad
- Keys: ASI:One https://asi1.ai/dashboard/api-keys · Agentverse https://agentverse.ai/profile/api-keys (values only in `.env`)

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
- No agent code yet.

## Status
- Tonight's prep (23 Oct): venv + packages installed and verified (AgentChatProtocol 0.3.0), examples cloned, repo scaffolded.
- Not done yet: API keys in `.env`, free-month offer claim, Sun-expert example run, Discord join, teammates agreed.

## Next steps (in order)
1. Create ASI:One and Agentverse API keys, put them in `.env`.
2. Claim offer code FETCHATHONIND (ASI:One Pro + Agentverse Premium).
3. Run the Sun-expert example from the ASI:One-compatible-agent doc once end to end.
4. Join Discord (channel Fetch-A-Thon 3.0) and agree roles with teammates.
5. On the day: decide the project after the 10:15 brief, build, submit by 16:30 to 17:50 (GitHub repo, Agentverse profile URL(s), public ASI:One chat URL, 3 to 5 min video, write-up, via Devpost).

## Open questions / waiting on others
- Who is on the team (email lists only Laksh as lead).
- Devpost link and where to submit.
- Results time: 12:15 (hackpack) vs 10:00 (ASI:One) on 28 Oct.

## Decisions not to undo
- Project idea is chosen by Laksh on the day, not before.
- Repo is public; no secrets ever committed.
- Commit small and push each one (Laksh said yes, 23 Oct 2026).

## Session log (newest first)
- 2026-10-23: scaffolded project, Python 3.11 venv, installed uagents/openai/python-dotenv, cloned fetchai/innovation-lab-examples to `C:\dev\fetchathon-ref`, added handoff automation.

<!-- handoff:auto:start -->
## Auto: repo state

_Refreshed 23 Oct 2026, 11:56 pm IST by `scripts/handoff.mjs` (runs on every commit). Don't edit inside this block._

Branch: `main` · remote: https://github.com/TheRealLaksh/fetchathon-3-agent.git

### Last 15 commits

- `fe9ea20` 2026-10-23 23:56 Add README with required badges, gitignore, env example and requirements

### Uncommitted changes at refresh time

```
A  .claude/settings.json
A  .githooks/pre-commit
A  CLAUDE.md
A  scripts/handoff.mjs
```
<!-- handoff:auto:end -->
