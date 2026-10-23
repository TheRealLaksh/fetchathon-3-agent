@HANDOFF.md

# Working on the Fetch-A-Thon 3.0 agent

- `HANDOFF.md` (imported above) is the project's memory across sessions. Start from it.
- **After every change, update `HANDOFF.md` before replying**: Status, Next steps, Open questions, Decisions, and a dated
  line in the Session log. Never edit inside the `handoff:auto` block; `scripts/handoff.mjs` rewrites it on each commit.
- A Stop hook (`.claude/settings.json`) blocks finishing a turn if project files are newer than `HANDOFF.md`.
- Git hooks live in `.githooks/` (`git config core.hooksPath .githooks`; re-run after a fresh clone).
- This repo is **public**. Never commit `.env`, API keys, seed phrases or tokens. Keys live only in `.env` (gitignored).
- Python 3.11 venv at `.venv` (uAgents does not support 3.14). Run with `.venv\Scripts\python.exe`.
- Laksh's vault notes: `C:\Users\laksh\OneDrive\Documents\Obsidian Vault\05 Resources\Fetch-A-Thon 3.0\` (start at "Fetch-A-Thon - Competition Brief (read this first)").
- Official reference examples are cloned (read-only) at `C:\dev\fetchathon-ref`.
