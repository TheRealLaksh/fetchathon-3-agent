# Prompt for the screen-recorded demo video: Mandi Net-Price Desk (about 4 min 15 s)

This replaces the motion-graphics brief (`docs/video-brag-prompt.md`). The video must look like a real **screen recording** of the product being used, with a voice-over.

How to use: open a NEW Claude Code session in `C:\dev\fetchathon-3` and paste only this launcher:

```
Read docs/video-screen-record-prompt.md completely and follow it exactly. Build the Mandi Net-Price Desk demo as a screen-recorded video with voice-over, using ffmpeg and Claude in Chrome. Ask me before installing anything.
```

Everything below is the brief. It is the source of truth.

---

## 0. Goal and rules

- **Deliverable:** `video-output/demo.mp4`, 1920x1080, 30 fps, **3:45 to 4:45** (hard limits 3:00 to 5:00), H.264 + AAC, with a clear voice-over and burned-in captions. Also `voiceover.txt`, `captions.srt`, `shotlist.md`, and `frames/` (one check frame per scene).
- **Look:** a real screen recording: browser and terminal windows, scrolling, clicking, typing. Calm and professional. No motion-graphics intro, no stock footage, no emojis, no hype words.
- **Honesty:** show only things that are real. Speed-ups must be labelled on screen ("sped up 4x"). Never present a re-created image as a live recording (label it). Never claim anything listed in section 7.
- **Privacy and safety:** never show or type API keys, `.env`, the Agentverse or ASI:One API-key pages, passwords, OTPs, or the account email address. Do not log in to anything, create accounts, change settings, post or send anything. Close the bookmarks bar and personal tabs before recording. Do not stop or restart the agents.
- **The ASI:One bot check:** repeated automated page loads made ASI:One show a reCAPTCHA. Open each ASI:One page **once**, wait for it, never refresh in a loop. If a reCAPTCHA or "Loading" screen persists after 2 minutes, stop and ask me (Laksh) to open that page by hand. Never try to solve or bypass a CAPTCHA.
- **Ask first** before installing software (ffmpeg, TTS packages) or doing anything not listed here.

## 1. Check the machine first (report before building)

1. `ffmpeg -version` (needed). If missing, propose `winget install Gyan.FFmpeg` and wait for my yes.
2. Claude in Chrome is connected (call `tabs_context_mcp`). If not, tell me.
3. The three agents are running: `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | ? { $_.CommandLine -match 'mandi\.' }` should list price_agent, logistics_agent, front_agent. If not, run `powershell -ExecutionPolicy Bypass -File scripts\start-agents.ps1`, then wait 90 seconds.
4. A voice for the narration. In order of preference: (a) I record my own voice later (then just produce `voiceover.txt` and a timing sheet), (b) Kokoro if already installed, (c) Windows built-in voices via `System.Speech` (no install). Tell me which you will use and play me nothing without asking. Keep each scene's audio as a separate WAV so a voice can be swapped without redoing the video.
5. One display, 1920x1080, scaling at 100%. If not, tell me before recording.

## 2. How to record (method)

Record **one clip per scene**, not one long take. For each scene: (1) generate that scene's narration audio and read its length, (2) start `ffmpeg` screen capture, (3) perform the scene's actions paced to the audio length, (4) stop, (5) mux the scene audio, (6) later concatenate all scenes. Scene video length = narration length + 0.8 s of lead-out.

Suggested capture command (adjust the offsets if the browser is not on the primary display):

```
ffmpeg -y -f gdigrab -framerate 30 -draw_mouse 1 -offset_x 0 -offset_y 0 -video_size 1920x1080 -i desktop -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p scene01.mp4
```

Run the capture in the background, do the browser or terminal actions, then stop it cleanly (send `q` to ffmpeg's stdin, or terminate it so the file is finalised). Check each clip plays and is not black (Chrome sometimes records black with window capture; use desktop capture as above).

Browser: maximise Chrome on the recorded display, hide bookmarks, zoom the page with CSS (`document.documentElement.style.zoom = '1.25'` via `javascript_tool`) so text is readable at 1080p. Scroll slowly (about 150 px per second) and pause 1 s on anything the narration names. Terminal: a fresh PowerShell window, font size 20 or larger, dark theme, `cls` first, working directory `C:\dev\fetchathon-3`, venv python as `.venv\Scripts\python.exe`.

Captions: write `captions.srt` from the narration timings and burn them in with the `subtitles` filter (white text, dark outline, bottom third, max 2 lines). Add a small lower-left tag on each scene (for example "Mandi Net-Price Desk" in scene 3) using `drawtext` only if it stays readable.

Optional polish (only if it stays clean): a slow 105% crop-zoom toward the highlighted row for 2 seconds, with `zoompan` or a crop filter. No fancy transitions: hard cuts or a 0.3 s fade.

## 3. Facts and data (all real, 24 Oct 2026)

Use `README.md`, `SOURCES.md`, `docs/writeup.md` and `mandi/selftest.py` in this repo as the reference for anything below.

- Tomato, seller in Gurugram, question `I have 25 tonnes of tomato in Gurugram. Where should I sell today?`. Ranked: Sohna APMC 2,500 price, 18 km, clears 2,443; Gohana APMC 2,500, 102 km, 2,411; Narnaul APMC 2,500, 113 km, 2,407; Patiala APMC 2,400, 261 km, 2,254; Dhand APMC 2,150, 189 km, 2,038; Machhiwara APMC 2,200, 323 km, 2,036 (Rs per quintal). Three mandis pay the same Rs 2,500; distance decides.
- For 8 tonnes the best choice versus the last shown is worth about Rs 32,500 (use only with the 8 tonne framing).
- Buyer mode, onion, restaurant in Delhi: ranks by landed cost. Earlier run: Sadhaura APMC 2,271 landed (price 2,200, about 199 km, marked with a tilde), Naraingarh APMC 2,790, Rohtak APMC 3,031. Prices move daily, so **use whatever the live agent returns when you record**, and fix the on-screen numbers and the narration to match (see section 6).
- Override: adding "my truck costs Rs 4 per tonne-km and my commission agent charges 6%" lowers Sohna's net (earlier 2,443 to 2,291). Again, use the live numbers.
- Assumptions in every reply: freight Rs 3.0 per tonne-km, mandi fee 2%, agent commission not included, transit loss 0.15 to 0.25% of value per drive hour; sources in `SOURCES.md`.
- Three agents: front agent `@mandi-desk` (mailbox, Agent Chat Protocol, ASI1 reads the request), Price Agent (data.gov.in), Logistics Agent (OpenStreetMap + OSRM). Addresses are in `README.md`. Ranking is plain code with 9 offline tests (`python -m mandi.selftest`).
- Reliability: saved price snapshot if the government API is down (tested live with a wrong key earlier); estimated routes if OSRM is down (covered by tests). Do not recreate the wrong-key test on screen: it would stop the live agent.

## 4. Before you record (prepare, then verify)

1. **ASI:One tomato chat.** Open the agent's ASI:One profile page once, ask the tomato question (25 tonnes), and leave that tab open. It takes 1 to 2 minutes for the agent to receive the message and the page may need one reload to show the reply (one reload is allowed; wait up to 2 minutes). Verify you can see the question, the ranked answer text and the "Plan this load" card with the page text. Only then record scene 3. Open it in its own tab at least 5 minutes before recording and do not touch it until the scene.
   - Profile URL: `https://asi1.ai/ai/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4`
   - If it cannot be made to load in time, use **Plan B for scene 3**: show the README "What an answer looks like" image, with an on-screen label "re-created from a real reply", and say so in the narration (`Here is a real answer, re-created from the agent's reply.`). Tell me you used Plan B.
2. **Pages to have ready** (open in tabs, do not reload them repeatedly): the GitHub README `https://github.com/TheRealLaksh/fetchathon-3-agent`, `SOURCES.md` on GitHub, and the three Agentverse profile pages listed in the README (open one at a time when you need it; these pages show the account email in the sidebar, so use the browser at a size or crop that keeps the sidebar out of frame, or crop that region out in post).
3. **Terminal runs** are real and take about 45 seconds each: `.venv\Scripts\python.exe -u -m mandi.chat_test "<question>"` (it talks to the live agent). Record the full run, then speed it up 4x in post (`setpts=PTS/4`) and put "sped up 4x" on screen.
4. Dry-run each scene once without recording to confirm timing and that nothing sensitive is on screen.

## 5. Storyboard (screen actions + narration)

Narration is calm and clear, about 2.1 words per second. Each scene's video length follows its audio. Target total about 255 s. Window lengths are guides.

**Scene 1 (0:00 to 0:14). Hook. GitHub README top.**
Screen: the README hero (banner, tagline, badge row). Slow scroll to the "What an answer looks like" image, pause on rows 1 to 3.
Narration: "Three mandis near Gurugram pay the same price for tomato today: two thousand five hundred rupees a quintal. Only one of them is the right place to sell."

**Scene 2 (0:14 to 0:38). The problem. README "at a glance" block.**
Screen: scroll up to the three-column block (The problem / What it does / What is different), pause on each column as it is named.
Narration: "The government publishes today's price at every mandi. But the highest price is rarely the best deal. You still pay for the drive, you lose some produce on the road, and you pay mandi fees. Working that out for every market means a spreadsheet and a lot of guessing, so most people sell where they always sell."

**Scene 3 (0:38 to 1:12). Ask in ASI:One. The pre-answered tomato chat (Plan B image if needed).**
Screen: the ASI:One chat tab. Scroll from the question to the ranked table, pause on row 1, scroll to the recommendation and the assumptions line, then to the interactive card.
Narration: "This is Mandi Net-Price Desk, an agent in ASI:One. You write one sentence. It reads the crop, the place and the quantity, pulls today's real mandi prices, and finds real road distances to each one. Then it ranks the mandis by what you actually clear per quintal. Sohna wins, with two thousand four hundred and forty three."

**Scene 4 (1:12 to 1:40). Why the order flips. Same chat or README image.**
Screen: pan across rows 1 to 4, pausing on the km column for Sohna (18) and Patiala (261) and on the "You actually clear" column.
Narration: "Sohna, Gohana and Narnaul all pay twenty five hundred. But Sohna is eighteen kilometres away, and the other two are over a hundred. After distance, transit loss and fees they clear two thousand four hundred and forty three, two thousand four hundred and eleven, and two thousand four hundred and seven. Patiala pays two thousand four hundred and clears only two thousand two hundred and fifty four."

**Scene 5 (1:40 to 1:56). What it is worth. The chat's recommendation line.**
Screen: the "For N quintals, picking ... is a difference of about Rs ..." sentence in the reply, highlighted by a slow zoom. Use the number the live reply shows; if the question was 25 tonnes the figure differs from the 8 tonne one, so say the figure that is on screen.
Narration (fill the number from the screen): "For this load, picking the best mandi over the last one shown is worth about [number on screen] rupees." If you want the 8 tonne framing, ask the 8 tonne question and say "thirty two thousand five hundred", matching the screen.

**Scene 6 (1:56 to 2:22). Buyers too. Terminal, live run.**
Screen: terminal, run `chat_test` with `I run a restaurant in Delhi. Where is onion cheapest to buy today?`. On-screen tag: "local test client, same agent, sped up 4x". Scroll to the table, pause on the cheapest row.
Narration: "It works the other way too. A restaurant in Delhi asks where onion is cheapest to buy. Here it is through our local test client, the same agent behind ASI:One. It ranks by landed cost: what you pay including freight and transit loss, not by sticker price. A tilde marks a distance that is approximate, because only the district could be located."
(Read the live numbers aloud only if you add them; otherwise keep the narration as is.)

**Scene 7 (2:22 to 3:02). Three agents. README architecture image, then Agentverse profiles.**
Screen: the architecture image in the README, then the front agent's Agentverse profile (banner, avatar, handle `@mandi-desk`, README with the two badges), then briefly the Price Agent and Logistics Agent profiles (Active, Local). Keep the email in the sidebar out of frame.
Narration: "Behind that one message are three separate agents on Fetch.ai. The front agent speaks the Agent Chat Protocol through an Agentverse mailbox, and uses the ASI one model only to understand the request. The Price Agent calls the government mandi dataset. The Logistics Agent gets real road routes from OpenStreetMap and OSRM. They pass each other typed messages. The ranking itself is plain code, not model output, so the numbers are repeatable, and nine offline tests check the maths."

**Scene 8 (3:02 to 3:36). Assumptions you can see and change. SOURCES.md, then terminal.**
Screen: `SOURCES.md` on GitHub (the table), pause on freight, market fee, commission. Then terminal: `chat_test` with `I have 25 tonnes of tomato in Gurugram, my truck costs Rs 4 per tonne-km and my commission agent charges 6%. Where should I sell?` (sped up 4x, labelled). Pause on the first row and the assumptions footer.
Narration: "Prices, locations and distances are real. Freight, mandi fee and transit loss are assumptions, and the reply lists every one with its source. Commission is left out unless you state it, because we could not find one reliable rate. Tell it your own numbers and it uses them: here, with a four rupee truck and six percent commission, the net for Sohna drops. And across every stress test we ran, the top of the ranking did not change."

**Scene 9 (3:36 to 3:56). Reliability. Terminal `selftest`, then the code.**
Screen: terminal `.venv\Scripts\python.exe -m mandi.selftest` (runs in seconds, ends with "9 tests passed"). Then GitHub `mandi/core.py`, scroll to `fetch_prices_with_source` (the snapshot fallback).
Narration: "If the government data source is down, the agent answers from the last saved snapshot and says so. If the routing service is down, it estimates distance and marks it approximate. Both fallbacks are covered by the nine tests you just saw, and we tested the price fallback live with a deliberately wrong key."

**Scene 10 (3:56 to 4:10). Honest limits. README "Known limits".**
Screen: the warning box and bullet list in README, slow scroll.
Narration: "It still runs on a laptop, the dataset holds only today's prices, and commission is excluded. Next, we host it on Agentverse and keep daily snapshots, so trend advice becomes possible."

**Scene 11 (4:10 to 4:20). Outro. Agentverse front profile or GitHub top.**
Screen: the front agent's Agentverse profile (banner and logo), then the repo URL in the address bar.
Narration: "Mandi Net-Price Desk. Find it in ASI:One as at mandi dash desk, and the code is on GitHub."

(About 530 words in total. If the voice runs long, shorten pauses first; never cut a number, a limit or a source.)

## 6. Keep numbers honest

Prices change daily. For scenes 3, 4, 5, 6 and 8: record first, read the numbers that actually appear, then **edit the narration text to match the screen** before generating that scene's audio. For scenes 3 and 4, if today's ranking differs from section 3, rewrite those lines with the real top three and the real distances, keeping the same message (same price, different distance). Never narrate a number that is not on screen in that scene.

## 7. Must NOT be shown or said

- Do not present the "Plan this load" button as a working feature. The card renders in ASI:One, but the tap is not confirmed end to end there. Show the card, do not click it.
- No real users, customers, savings, testimonials or adoption claims. The only money figure allowed is the one shown by the live reply on screen.
- Do not say it is instant. If ASI:One needed time, the video may cut, but do not claim speed.
- Do not say it predicts prices or advises when to wait. It does not (the dataset has no history).
- Do not call the assumptions "data" or "official".
- No emojis, no hype words (revolutionary, game-changing, seamless, supercharge).
- Do not show API keys, `.env`, the account email, or other private data. Do not show other ASI:One chats, notifications or personal tabs.
- Do not use any Fetch.ai, ASI:One, Masters' Union or data.gov.in logos except as they appear on their own pages in the recording.

## 8. Quality checks before delivering

1. Extract one frame per scene (`ffmpeg -ss <mid> -i demo.mp4 -frames:v 1 frames/sceneNN.png`) and look at each: legible text, no private data, no CAPTCHA, no black frames, captions inside the safe area.
2. Total length is within 3:45 to 4:45, audio is clear, narration matches what is on screen, speed-ups are labelled.
3. `captions.srt` matches the audio.
4. Write `shotlist.md`: scene, URL or command, exact actions, narration. This lets me re-record any scene by hand with Recordly (https://github.com/webadderall/Recordly, a free screen recorder with auto-zoom) or any recorder if you cannot finish the automated version.
5. Report: file locations, final length, which scenes used Plan B, which numbers were taken live, and anything I should check by hand. Offer to re-record any single scene.
6. Do not upload or publish the video anywhere. I will do that.

## 9. If something blocks you

- ASI:One shows a CAPTCHA or will not load: stop, say which scene, and ask me to open that page by hand; use Plan B for scene 3 meanwhile.
- ffmpeg or a voice is not available and I say no to installing: produce `shotlist.md` and `voiceover.txt` and stop.
- Never work around a safety or privacy rule in this file. Ask me instead.
