# Prompt for the /brag video session: Mandi Net-Price Desk demo (about 4 min 15 s)

How to use: open a NEW Claude Code session in `C:\dev\fetchathon-3`, then paste only this launcher line:

```
/brag --full --voice --tone polished --format landscape --duration 255 Read docs/video-brag-prompt.md completely first and follow it exactly. This is a 4 minute hackathon demo video, NOT the usual 20 second brag, so the 15 to 25 second rules, the "short" creative law and the 15 to 25 second storyboard gate are overridden by this file.
```

Everything below is the brief. Treat it as the source of truth.

---

## 0. Overrides to the brag skill

- **Length:** target 255 seconds (4:15). Acceptable range 225 to 285. The Fetch-A-Thon rule is 3 to 5 minutes, never go under 3:00 or over 5:00. Scene durations must sum to the target. Ignore any "15 to 25 seconds" gate.
- **Voice:** narration ON (Kokoro via Hyperframes). Use the narration text in section 4 verbatim, scene by scene; do not paraphrase numbers. Also write the narration to `voiceover.txt` so a human can record over it instead.
- **Tone:** `polished`: serious, elegant, restrained, long holds, soft fades. Confident and warm, not hype, no jokes, no "revolutionary".
- **Format:** landscape 1920x1080, 30 fps. Burn in readable captions that follow the narration.
- **Music:** one soft instrumental bed, mixed low under the voice (voice always clear), gentle build into the outro. Sound effects minimal and soft (a quiet tick when a table row lands, a soft chime at the recommendation).
- **Output:** `brag-output/` in the repo (add `brag-output/` to `.gitignore` if it is not there). Deliver `brag.mp4`, `brag.jpg` poster, `voiceover.txt`, `captions.srt`, `share-copy.txt`.
- **Hard rule on honesty:** nothing may be shown or said that is not in section 3 (facts) or section 6 (what not to say). No invented users, savings, testimonials, statistics or screenshots presented as real.

## 1. What the product is, in one breath

Mandi Net-Price Desk is an agent in ASI:One. A produce trader types one sentence ("I have 25 tonnes of tomato in Gurugram. Where should I sell today?") and gets the mandis ranked by what they actually clear after real road freight, transit loss and mandi fees, using today's real government prices. Buyers get landed cost instead. It is three cooperating agents on Fetch.ai (Agentverse, Agent Chat Protocol, ASI1 model) with live data from data.gov.in, OpenStreetMap and OSRM.

Built by team fetchathon3.0-5865 at Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union Gurugram, 24 Oct 2026): Laksh Pradhwani (lead), Mark Patel, Aryan Rao, Saiansh Kathuria.

## 2. Visual identity (use exactly)

- Colours: deep green `#0F3D2E` to `#1F6B4F` diagonal gradient as the base; amber `#F2B84B` as the accent (route lines, highlights, the recommended row); white for primary text; mint `#B2DEC8` for secondary text. Dark cards on the gradient: `rgba(255,255,255,0.06)` with a thin mint border.
- Fonts: Georgia Bold for titles (as in `assets/banner.png`), a clean humanist sans (Inter or system sans) for body and table text. Tabular numerals in tables.
- Real assets to reuse: `assets/pfp.png` (logo mark: three rising white bars with an amber route line) and `assets/banner.png`. Re-draw the mark as vector for large use rather than upscaling the PNG.
- No emojis, no unicode glyphs used as icons. Use a proper icon set (Phosphor) if an icon is needed. No stock footage, no generic "SaaS" language.
- Motion: things appear one by one, rows land in sequence, numbers count up, the amber route line draws between points. Slow, even easing. Every frame should be clean enough to screenshot.
- Layout: generous margins, one idea per scene, large type. Every line of on-screen text must stay fully visible about 0.3 s per word after it finishes appearing.

## 3. Facts and data you may use (all real, from 24 Oct 2026)

### The headline example (tomato, seller in Gurugram)

Question typed by the user: `I have 25 tonnes of tomato in Gurugram. Where should I sell today?`
(Quantity is 250 quintals. The first reply line is "Checking today's Tomato prices near Gurugram, Haryana and the real road routes.")

Ranked result (modal price in Rs per quintal, real road km from Gurugram, drive hours, net the trader clears per quintal):

| # | Mandi | Price | Road km | Drive h | You actually clear |
|---|---|---|---|---|---|
| 1 | Sohna APMC (Gurgaon, Haryana) | 2,500 | 18 | 0.3 | 2,443 |
| 2 | Gohana APMC (Sonipat, Haryana) | 2,500 | 102 | 1.4 | 2,411 |
| 3 | Narnaul APMC (Mahendragarh-Narnaul, Haryana) | 2,500 | 113 | 1.4 | 2,407 |
| 4 | Patiala APMC (Patiala, Punjab) | 2,400 | 261 | 3.3 | 2,254 |
| 5 | Dhand APMC (Kaithal, Haryana) | 2,150 | 189 | 2.4 | 2,038 |
| 6 | Machhiwara APMC (Ludhiana, Punjab) | 2,200 | 323 | 4.2 | 2,036 |

- Three mandis pay the same Rs 2,500 per quintal. The net figures differ because of distance.
- For 80 quintals (8 tonnes) the best choice versus the last one shown is worth about Rs 32,500. (Use only for the 8 tonne framing. Do not combine with the 25 tonne example.)
- The reply ends with the assumptions it used and a note that prices are the data.gov.in daily mandi data dated 24/10/2026.

### Buyer mode (onion, restaurant in Delhi)

Question: `I run a restaurant in Delhi. Where is onion cheapest to buy today?` The ranking is by landed cost (price + freight + transit loss), lowest first:

| # | Mandi | Price | Road km | You pay (landed) |
|---|---|---|---|---|
| 1 | Sadhaura APMC (Yamuna Nagar, Haryana) | 2,200 | about 199 | 2,271 |
| 2 | Naraingarh APMC (Ambala, Haryana) | 2,700 | 247 | 2,790 |
| 3 | Rohtak APMC (Rohtak, Haryana) | 3,000 | 78 | 3,031 |

(`about 199` means the mandi was located only by its district centre, so the distance is approximate and the agent marks it with a tilde. Show the tilde.)

### Override example

Same tomato question plus "my truck costs Rs 4 per tonne-km and my commission agent charges 6%": Sohna's net drops from Rs 2,443 to Rs 2,291 per quintal. The agent applies the user's numbers and says so.

### Assumptions and where they come from (see SOURCES.md)

- Freight Rs 3.0 per tonne-km: derived from long-haul rates Rs 2.8 to 3.7 per tonne-km (Business Standard / CMIE, April 2024; FR8 route quotes). Short hauls usually cost more.
- Market fee 2%: Haryana fruit and vegetable market fee 1% plus Rural Development Fund 1% (Tribune, Feb 2024).
- Agent commission: not included by default, because no reliable single rate was found; the user can state theirs.
- Transit loss: 0.25% of value per drive hour for tomato, 0.15% for onion, 0.2% otherwise, derived from NABCONS 2022 loss figures (our own scaling).
- Sensitivity: the top four mandis (Sohna, Gohana, Narnaul, Patiala) kept the same order when freight went to Rs 3.7 and Rs 5.0, transit loss to 0.5% per hour, and fees plus commission to 8%.

### How it is built

- Three separate agents that send each other typed messages:
  1. **Mandi Net-Price Desk** (front agent, handle `@mandi-desk`, address `agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4`): Agent Chat Protocol, Agentverse mailbox. Uses the ASI1 model only to read the request (crop, place, sell or buy, quantity). Ranks and replies.
  2. **Mandi Price Agent** (`agent1qdppp6kky9mlmq9j4c7v0nksqpvusy7w9vjxylzuu6xt48fs20mw7ecwcp0`): today's real modal prices from the data.gov.in daily mandi dataset.
  3. **Mandi Logistics Agent** (`agent1qtw0yw8kanxv48wd0v2zrhdg4p6ewersauhstygfy4s2qv20fyxkjl8w9y3`): locates mandis with OpenStreetMap and gets real road distance and drive time from OSRM.
- The ranking maths is plain code, not LLM output, covered by 9 offline tests (`python -m mandi.selftest` prints nine "ok" lines and "9 tests passed").
- Fetch.ai pieces: uAgents, Agentverse, Agent Chat Protocol, ASI1 LLM, agent-to-agent messages, ASI:One interactive card.

### Reliability

- If the government API is unreachable, the agent answers from the last saved snapshot and says so: "Live government prices were unreachable, so this uses the last saved snapshot ... Treat it as possibly stale." Tested live by giving the Price Agent a wrong API key.
- If the routing service is down, distances are estimated from straight-line distance and marked approximate.
- A cache warm-up script pre-loads map lookups so the first question is fast.

### Honest limits (these go in the video)

- The agents run on a laptop for now; the mailbox agent answers only while all three are running.
- The dataset holds only today's prices, so no trend and no "wait and sell later" advice.
- Distances for some mandis are approximate (district centre), marked `~`.
- Agent commission is excluded unless the user states it.

### Links to show in the outro

- Handle: `@mandi-desk` in ASI:One
- Repo: github.com/TheRealLaksh/fetchathon-3-agent
- Team ID: fetchathon3.0-5865

## 4. Storyboard and narration (total 255 s)

Narration is spoken by one calm, clear voice. Each scene lists duration, visuals, on-screen text and the exact narration. Pace the voice at about 2.3 words per second; leave natural pauses at the cuts. Captions mirror the narration.

**Scene 1. Hook (0:00 to 0:14, 14 s).**
Visual: dark green field. The question types out in a chat bubble: "I have 25 tonnes of tomato in Gurugram. Where should I sell today?" Below it, three white bars appear, each labelled "Rs 2,500 per quintal": Sohna, Gohana, Narnaul.
On-screen: "Three mandis. Same price."
Narration: "Three mandis near Gurugram pay the same price for tomato today: two thousand five hundred rupees a quintal. Only one of them is the right place to sell."

**Scene 2. The problem (0:14 to 0:38, 24 s).**
Visual: the sticker price shrinks as cost items slide in under it as amber lines: "the drive", "produce lost on the road", "mandi fees". A truck-route line draws across the screen.
On-screen: "The highest price is not the best deal."
Narration: "The government publishes today's price at every mandi. But the highest price is rarely the best deal. You still pay for the drive, you lose some produce on the road, and you pay mandi fees. Working that out for every market means a spreadsheet and a lot of guessing, so most people sell where they always sell."

**Scene 3. Ask in ASI:One (0:38 to 1:12, 34 s).**
Visual: an ASI:One style chat (re-created from the real reply text; mark it subtly "re-created from a real reply"). The agent's first line appears: "Checking today's Tomato prices near Gurugram, Haryana and the real road routes." Then the ranked table lands row by row with the real numbers from section 3. The "You actually clear" column is highlighted in amber and the first row is outlined.
On-screen: "Mandi Net-Price Desk, @mandi-desk". Show row 1 outlined.
Narration: "This is Mandi Net-Price Desk, an agent in ASI:One. You write one sentence. It reads the crop, the place, and the quantity, pulls today's real mandi prices, and finds real road distances to each one. Then it ranks the mandis by what you actually clear per quintal. Sohna wins, with two thousand four hundred and forty three."

**Scene 4. Why the order flips (1:12 to 1:40, 28 s).**
Visual: four pairs of bars (price vs what you clear) for Sohna, Gohana, Narnaul, Patiala, with the km under each: 18, 102, 113, 261. Gaps open up as the distance grows. Amber route line connects Gurugram to each.
On-screen: "Same sticker price. Different distance."
Narration: "Sohna, Gohana and Narnaul all pay twenty five hundred. But Sohna is eighteen kilometres away, and the other two are over a hundred. After distance, transit loss and fees they clear two thousand four hundred and forty three, two thousand four hundred and eleven, and two thousand four hundred and seven. Patiala pays two thousand four hundred and clears only two thousand two hundred and fifty four."

**Scene 5. What it is worth (1:40 to 1:56, 16 s).**
Visual: a single large number counts up: "Rs 32,500" with the label "for 8 tonnes, best choice versus the last one shown".
Narration: "For eight tonnes, picking the best mandi over the last one shown is worth about thirty two thousand five hundred rupees."

**Scene 6. Buyers too (1:56 to 2:22, 26 s).**
Visual: new chat: "I run a restaurant in Delhi. Where is onion cheapest to buy today?" Table by landed cost: Sadhaura 2,271 (price 2,200, about 199 km, show the tilde), Naraingarh 2,790, Rohtak 3,031. The cheapest row outlined.
On-screen: "Buyers get landed cost."
Narration: "It works the other way too. A restaurant in Delhi asks where onion is cheapest to buy. The agent ranks by landed cost: what you pay including freight and transit loss, not by sticker price. A tilde marks a distance that is approximate, because only the district could be located."

**Scene 7. Three agents (2:22 to 3:02, 40 s).**
Visual: architecture animation. Left to right: ASI:One chat, Agentverse mailbox, the front agent "Mandi Net-Price Desk" in the centre. From the front agent, two arrows go out: to "Price Agent" (label: data.gov.in daily mandi prices) and to "Logistics Agent" (label: OpenStreetMap and OSRM road routes). Small tag on the front agent: "ASI1 reads the request". Below, a strip: "Ranking is plain code. 9 offline tests." Show the three agent names with shortened addresses (first 10 and last 6 characters).
Narration: "Behind that one message are three separate agents on Fetch.ai. The front agent speaks the Agent Chat Protocol through an Agentverse mailbox, and uses the ASI one model only to understand the request. The Price Agent calls the government mandi dataset. The Logistics Agent gets real road routes from OpenStreetMap and OSRM. They pass each other typed messages. The ranking itself is plain code, not model output, so the numbers are repeatable, and nine offline tests check the maths."

**Scene 8. Trust: assumptions you can see and change (3:02 to 3:36, 34 s).**
Visual: the assumptions card as printed in the real reply (freight, mandi fee, agent commission, transit loss), each with a short source tag (Business Standard and CMIE, Tribune, NABCONS 2022). Then a second chat line: "my truck costs Rs 4 per tonne-km and my commission agent charges 6%" and Sohna's net animates from 2,443 to 2,291.
On-screen: "Prices are real. Costs are assumptions you can see and change."
Narration: "Prices, locations and distances are real. Freight, mandi fee and transit loss are assumptions, and the reply lists every one with its source. Commission is left out unless you state it, because we could not find one reliable rate. Tell it your own numbers and it uses them: with a four rupee truck and six percent commission, Sohna drops to two thousand two hundred and ninety one. And across every stress test we ran, the top of the ranking did not change."

**Scene 9. Reliability (3:36 to 3:56, 20 s).**
Visual: a terminal-style card showing `python -m mandi.selftest` ending with "9 tests passed", then the real fallback line: "Live government prices were unreachable, so this uses the last saved snapshot. Treat it as possibly stale."
Narration: "If the government data source is down, the agent answers from the last saved snapshot and says so. If the routing service is down, it estimates distance and marks it approximate. We tested the price fallback live with a deliberately wrong key."

**Scene 10. Honest limits and next steps (3:56 to 4:10, 14 s).**
Visual: two short lists, restrained. "Today": runs on a laptop; today's prices only, no trend; commission excluded. "Next": host on Agentverse; daily snapshots for trend and wait-or-sell; per-state fee table.
Narration: "It still runs on a laptop, the dataset holds only today's prices, and commission is excluded. Next, we host it on Agentverse and keep daily snapshots, so trend advice becomes possible."

**Scene 11. Outro (4:10 to 4:15, 5 s, hold if audio needs a beat more).**
Visual: the logo mark draws in, then the banner line: "Mandi Net-Price Desk". Below: "@mandi-desk in ASI:One", "github.com/TheRealLaksh/fetchathon-3-agent", "Team fetchathon3.0-5865: Laksh Pradhwani, Mark Patel, Aryan Rao, Saiansh Kathuria", "Fetch-A-Thon 3.0".
Narration: "Mandi Net-Price Desk. Find it in ASI:One as at mandi dash desk."

(Total narration is about 540 words. If the rendered voice runs long, trim pauses first, then shorten the visual holds; never cut a number, a limit or a source.)

## 5. Optional real screen recordings

If Laksh adds clips to `assets/clips/` (for example `asi1-tomato.mp4`, `agentverse-profile.mp4`), use them in scene 3 and scene 7 as picture-in-picture or full-frame inserts, and keep the re-created chat as the fallback. Never pass a re-created chat off as a recording. Do not film, log in to, or screenshot ASI:One yourself: ASI:One shows a bot check after repeated automated loads.

## 6. What must NOT be shown or said

- Do not say or show the "Plan this load" button as a working feature. It renders in ASI:One but the tap is not confirmed end to end there.
- Do not claim real users, customers, savings figures, testimonials or adoption. The only money figure allowed is the Rs 32,500 example above, tied to 8 tonnes.
- Do not say or imply the answer is instant. If you show timing, show the "Checking today's prices..." line before the result.
- Do not say it predicts prices or advises when to wait. It does not (the dataset has no history).
- Do not call the assumptions "data" or "official". They are assumptions with sources.
- No emojis, no em dashes in `share-copy.txt`, no "excited to share", no hype words (revolutionary, game-changing, seamless, supercharge).
- Do not invent logos of Fetch.ai, ASI:One, Masters' Union or data.gov.in. Use plain text labels for them.

## 7. Deliverables checklist

1. `brag-plan.md` with the storyboard above (adjusted only for timing).
2. Composition in `brag-output/composition/` passing `npx hyperframes check` with zero errors.
3. `brag.mp4` (1920x1080, 30 fps, 3:45 to 4:45), `brag.jpg` poster (a settled frame, such as the ranked table with row 1 outlined) baked as frame 0.
4. `voiceover.txt`, `captions.srt`.
5. `share-copy.txt`: 2 to 3 sentences for LinkedIn, specific, no emojis, no em dashes, mentions the Rs 2,500 versus net example and `@mandi-desk`.
6. Tell Laksh where the files are, give one sentence on the creative angle, and offer to re-time any scene.
