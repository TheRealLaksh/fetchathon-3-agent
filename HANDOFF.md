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
000. Demo video is built (`brag-output/brag.mp4`): watch it through, decide the scene 8 wording (see "Demo video"), upload it for Devpost (3 to 5 min rule: it is 4:15).
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

## Screen-recorded demo video (made 24 to 25 Oct 2026, by Claude from `docs/video-screen-record-prompt.md`)
- Output in `video-output/` (read `STATUS.md` there first): `demo.mp4` (1920x1080, 30 fps, about 4:44, Zira voice-over, burned-in captions), `captions.srt`, `voiceover.txt`, `shotlist.md` (every scene's URL/command/actions/narration, for re-recording by hand), `frames/` (one check frame per scene), `clips/` (per-scene clips + raw captures), `audio/` (one WAV per scene, so the voice can be swapped), `tools/` (build scripts: `build_term_scenes.py`, `build_final.py`, `build_shotlist.py`, `term-run.ps1`, `tts.ps1`).
- Real recording of Brave (Claude in Chrome) and Windows Terminal via ffmpeg gdigrab 2560x1440 -> 1080p. Scene 3 and 4 use the live ASI:One chat (https://asi1.ai/chat/50a184bf-3b9c-4a31-a2ca-e8218ce5b898, sent 22:56 on 24 Oct); Plan B was not needed. Terminal waits in scenes 5, 6, 8 are sped up 8x and labelled.
- The live data.gov.in rows move through the day (tomato top was Bassi, then Kurali, then Sonepat), so each scene narrates only its own screen. Scene 1 uses the README example image (8 tonnes), worded "in this example run".
- Open: the Price and Logistics Agentverse profiles show no name/README after the 22:52 restart (only Active and Local); the narration claim "tested the price fallback live with a deliberately wrong key" is from earlier work (HANDOFF 24 Oct 15:30), not re-shown. Video not uploaded anywhere.

## Demo video (made 24 Oct 2026, ~16:40, via /brag)
- Output (gitignored, local only): `brag-output/` = `brag.mp4` (1920x1080, 30 fps, 4:15, narrated, captioned), `brag.jpg` poster, `voiceover.txt` (verbatim narration per scene, for a human re-record), `captions.srt`, `share-copy.txt`, `brag-plan.md`, `composition-brief.md`, `composition/` (Hyperframes project, `npx hyperframes check` = 0 errors).
- Source of truth for content: `docs/video-brag-prompt.md`. Pipeline to re-time or edit a scene: `brag-output/build/` (`script.json` narration + scene lengths, `make_vo.py` Kokoro clips per sentence + timeline + captions, `index.template.html`, `build_comp.py`). Run with `C:\dev\kokoro-venv\Scripts\python.exe` (separate venv with kokoro-onnx, not the project `.venv`), then `npx hyperframes check` and `npx hyperframes render --quality high --output ../brag.mp4` from `brag-output/composition`.
- Narration is Kokoro `af_heart`, speed 0.86, loudness-normalised to -16 LUFS. It was not listened to by Claude: check how it says Sohna, Gohana, Narnaul, mandi, quintal, OSRM; if any is off, record over `voiceover.txt` or respell in `script.json`.
- The ASI:One chat is a re-created panel (labelled), never a recording. Real reply text comes from `mandi/ranking.py` and `mandi/front_agent.py`. `Plan this load` is not shown anywhere.
- Known wording issue to decide: scene 8 narration (verbatim from the brief) says the reply "lists every one with its source". The real reply names the basis (e.g. "Haryana market fee plus RDF") but the named sources (Business Standard/CMIE, Tribune, NABCONS) are in SOURCES.md, not in the reply text. Suggested fix: "and the repo lists every one with its source" (re-run `make_vo.py`, `build_comp.py`, render).

## Session log (newest first)
- 2026-10-25 (~01:15): SCREEN-RECORDED DEMO VIDEO BUILT (`video-output/demo.mp4`, about 4:44) from the screen-record brief; agents were restarted at 22:52 (PC sleep killed them); deadline is now 10:00 AM Sun 25 Oct (mail 22:52). No code changed. See "Screen-recorded demo video".
- 2026-10-24 (~16:40): VIDEO BUILT with /brag (see "Demo video" above). 11 scenes, 255 s, Hyperframes check 0 errors, contrast 89/89. Nothing in the code changed. Still to do by Laksh: watch it through, upload it for Devpost, decide the scene 8 wording above, optionally add real screen clips to `assets/clips/` for scenes 3 and 7.
- 2026-10-24 (~16:20): README redesigned and checked on the live GitHub page: centered hero + badge row + nav links, at-a-glance 3-column block, answer image (assets/example-answer.png, re-created from a real reply), branded architecture image (assets/architecture.png), agents as readable blocks with copyable addresses, collapsible Run and File map sections, NOTE and WARNING callouts. Required badge lines kept exactly at the top. Images are generated with Pillow (scripts live only in the session scratchpad; regenerate by hand if numbers change).
- 2026-10-24 (~15:58): README reviewed against the hackpack and rewritten (submission links table, requirements map, bonus map, test-without-keys, key sources, mailbox connect steps, extra resources). FOUND: Agentverse agent READMEs lacked the Innovation Lab badges -> added docs/agent-readme-{front,price,logistics}.md + mandi/branding.py (readme, description, avatar, banner published from code). For a mailbox agent the profile is only pushed on /connect: re-ran POST /connect (key from .env); this REPLACED the hand-typed README (now badges render) and CLEARED starter prompts (re-added by hand). Agents restarted; end-to-end still works. NOTE: after any front-agent re-connect, re-add starter prompts. Helper agents' Agentverse profiles not re-checked after restart.
- 2026-10-24 (~16:00): SUBMISSION DOCS written: README (agent table, how it works, run steps, limits), docs/writeup.md (Devpost text), docs/video-script.md (4 min script + pre-flight), docs/submission-checklist.md. STILL TO DO BY LAKSH: share the ASI:One chat publicly (his browser) and paste link; record + upload video; fill Devpost form; keep the three agent processes running.
- 2026-10-24 (~15:50): Agentverse profile finished: avatar (assets/pfp.png) + banner (assets/banner.png) uploaded, handle @mandi-desk set, setup checklist complete. ASI:One still shows the old name/avatar 'ASI-agent' (its own cache; check again later). CARD TAP FINDINGS: ASI:One -> mailbox -> agent delivery takes ~1.5 min each way and the chat page needs a reload (20-90 s) to show replies, so an earlier 'tap did nothing' was probably me restarting the agent before the tap arrived (LAST list is in memory and lost on restart). Do NOT restart the front agent while testing. A tap in a chat whose 'To' is the ASI:One assistant may be routed to it instead of our agent (unconfirmed). After many reloads ASI:One showed a Loading screen with a reCAPTCHA (bot check): stop automated reloads; test the tap by hand. The agent logs every incoming message text ('incoming from ...') so the tap format can be read from the log.
- 2026-10-24 (~15:30): added offline fallbacks (saved price snapshot, estimated routes), interactive card (custom card, "Plan this load" button per mandi), load planner (trucks, totals, optional spread across top 3), 9 offline self-tests (python -m mandi.selftest). VERIFIED: card renders in ASI:One; snapshot fallback works with a wrong API key; JSON card tap -> plan works locally (TAP=2 chat_test). NOT CONFIRMED: tapping the card in the ASI:One UI did not produce a plan within ~3 min (tap goes to ASI:One's planner, 'Submitted' shown, agent log shows nothing). Typed 'plan the load for <mandi>' is handled instead. 'Sell now vs wait' NOT built: data.gov.in API returns only today's rows (date filter ignored, verified), so no history; dated snapshots now accumulate in mandi/snapshots/ (gitignored). ASI:One chat view needs a page reload to show new agent messages (UI quirk).
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

_Refreshed 24 Oct 2026, 11:50 pm IST by `scripts/handoff.mjs` (runs on every commit). Don't edit inside this block._

Branch: `main` · remote: https://github.com/TheRealLaksh/fetchathon-3-agent.git

### Last 15 commits

- `cd619e7` 2026-10-24 16:28 Add screen-recorded video brief (replaces the motion-graphics one)
- `5e27d1b` 2026-10-24 16:24 README: list all three Agentverse profile links in the submission table
- `e34e678` 2026-10-24 16:10 Soften restart note in checklist
- `61bba0c` 2026-10-24 16:09 Add start and stop scripts for the three agents
- `5af8f0d` 2026-10-24 16:09 Record README redesign in handoff
- `8d4f549` 2026-10-24 16:08 README: branded architecture image instead of the mermaid diagram
- `30ac115` 2026-10-24 16:07 README: agents as readable blocks instead of a wide table
- `d8d6391` 2026-10-24 16:05 README: centered hero, at-a-glance block, answer image, architecture diagram, collapsible sections
- `92901b9` 2026-10-24 15:56 README review fixes: badges in agent READMEs, run and test steps, submission links
- `8c8da6f` 2026-10-24 15:50 Add detailed video brief for the /brag session
- `1117198` 2026-10-24 15:47 Add submission docs: README, write-up, video script, checklist
- `62ce375` 2026-10-24 15:44 Add profile picture and banner, log incoming messages, record card-tap findings
- `7b3ad1e` 2026-10-24 15:27 Handle ASI:One prose card taps and typed load-plan requests; extend tests
- `1e97713` 2026-10-24 15:11 Add interactive card, load planner and offline self-tests
- `4d33d2c` 2026-10-24 15:11 Add offline fallbacks: saved price snapshot and estimated routes

### Uncommitted changes at refresh time

```
M  HANDOFF.md
A  video-output/shotlist.md
A  video-output/tools/build_final.py
A  video-output/tools/build_shotlist.py
A  video-output/tools/build_term_scenes.py
A  video-output/tools/mux.ps1
A  video-output/tools/place-window.ps1
A  video-output/tools/term-run.ps1
A  video-output/tools/tts.ps1
```
<!-- handoff:auto:end -->
