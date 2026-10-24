# Submission checklist (Devpost)

Deadline per the hackpack: between 16:30 and 17:50 on Sat 24 Oct 2026. Do the items in order.

## 1. Shared ASI:One chat link (you must do this in your own browser)

The chat has to show the whole workflow: question, ranked answer, card.

1. Open ASI:One signed in as yourself and open the chat titled "Tomato Sales Location In Gurugram" that contains the full answer and the card (the chat from about 15:23). If the page is slow or shows a check, wait and retry once; do not reload repeatedly.
2. Use the chat's Share option (the chat title menu or the share icon) and set the link to public.
3. Copy the link, open it in a private or incognito window, and confirm the table and card are visible without logging in.
4. Paste it into `docs/writeup.md` under Links and into the Devpost form.

If sharing is not offered for that chat, start a fresh chat from the agent's profile page, ask the tomato question, wait about two minutes, reload, then share.

## 2. Links to paste

| Item | Value |
|---|---|
| GitHub repo (public) | https://github.com/TheRealLaksh/fetchathon-3-agent |
| Front agent in ASI:One | https://asi1.ai/ai/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4 |
| Agentverse profile, front agent | https://agentverse.ai/agents/details/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4/profile |
| Agentverse profile, Price Agent | https://agentverse.ai/agents/details/agent1qdppp6kky9mlmq9j4c7v0nksqpvusy7w9vjxylzuu6xt48fs20mw7ecwcp0/profile |
| Agentverse profile, Logistics Agent | https://agentverse.ai/agents/details/agent1qtw0yw8kanxv48wd0v2zrhdg4p6ewersauhstygfy4s2qv20fyxkjl8w9y3/profile |
| Public ASI:One chat | (from step 1) |
| Demo video | (upload, then paste) |
| Write-up | `docs/writeup.md` (paste the text into Devpost) |

## 3. Demo video

Follow `docs/video-script.md` (about 4 minutes, limit 3 to 5). Ask the demo questions in ASI:One before recording.

## 4. Before you submit

- [ ] README has both badges (`tag:innovationlab`, `tag:hackathon`), the agent table with names and addresses, and run instructions. Done.
- [ ] Repo is public and has no `.env` or keys. Check with `git ls-files | grep -i env` (only `.env.example` should appear).
- [ ] The three agent processes are running and stay running until the results are out. Keep the laptop plugged in with sleep turned off. To restart after a reboot: `powershell -ExecutionPolicy Bypass -File scripts\start-agents.ps1` (stop first with `scripts\stop-agents.ps1`). The mailbox connection survived every restart today, but wait about a minute before asking a question and test once.
- [ ] Do not restart the front agent after recording (it forgets the last ranking in memory).
- [ ] Join the Fetch-A-Thon Discord and watch for any announcement about the submission form.

## 5. Mandatory items from the hackpack, status

| Requirement | Status |
|---|---|
| Registered on Agentverse | Front agent (mailbox) and both helper agents (local) have profiles |
| Agent Chat Protocol | Yes, front agent |
| Discoverable and usable in ASI:One | Yes, mention it by address or open its profile in ASI:One |
| Real tool use or multi-agent | Both: live data APIs and three cooperating agents |
| Whole workflow inside ASI:One | Question, answer and card are in ASI:One (card tap unconfirmed) |
| Public GitHub repo | Yes |
| Public ASI:One chat URL | Needs step 1 |
| 3 to 5 minute video | Needs recording |
| Short write-up | `docs/writeup.md` |
