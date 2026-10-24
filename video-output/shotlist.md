# Shot list: Mandi Net-Price Desk demo (screen recording)

Recorded 24 to 25 Oct 2026. Capture: ffmpeg gdigrab 2560x1440 from the top-left of a 2560x1600 display, scaled to 1920x1080, 30 fps. Brave window with only Claude's tab group (bookmarks bar hidden), terminal = Windows Terminal. Narration: Windows "Microsoft Zira Desktop" voice, one WAV per scene in `audio/`, played 1.04x in the final cut.

Live numbers change through the day (data.gov.in): scenes 3, 4, 5, 6 and 8 narrate only what was on screen at the time of recording. Re-record those scenes and rewrite their text from the new screen if you redo them.

Speed-ups: the terminal waits in scenes 5, 6 and 8 are sped up 8x and labelled on screen. Nothing else is sped up (apart from the global 1.04x).

## Scene 1: Hook: README hero, then the example answer image

- **URL or command:** `https://github.com/TheRealLaksh/fetchathon-3-agent/blob/main/README.md`
- **Actions:** Browser zoom 125%. Start at the README top (banner, tagline, badges). After about 8 s scroll slowly down to the "What an answer looks like" image and stop with rows 1 to 3 in view. The image is the 8-tonne example from the README, not today's live answer, so the narration says "in this example run".
- **Narration:** Which mandi should you sell at? In this example run, three mandis near Gurugram paid the same price for tomato: two thousand five hundred rupees a quintal. But each one clears a different amount once distance is counted, and only one is the right place to sell.

## Scene 2: The problem: README at-a-glance block

- **URL or command:** `https://github.com/TheRealLaksh/fetchathon-3-agent/blob/main/README.md`
- **Actions:** Browser zoom 125%. Show the badge row and the three-column block (The problem / What it does / What is different); scroll down by about 80 px over the whole scene.
- **Narration:** The government publishes today's price at every mandi. But the highest price is rarely the best deal. You still pay for the drive, you lose some produce on the road, and you pay mandi fees. Working that out for every market means a spreadsheet and a lot of guessing, so most people sell where they always sell.

## Scene 3: Ask in ASI:One: the live tomato chat

- **URL or command:** `https://asi1.ai/chat/50a184bf-3b9c-4a31-a2ca-e8218ce5b898  (after sending: @agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4 I have 25 tonnes of tomato in Gurugram. Where should I sell today?)`
- **Actions:** Send the question from the agent profile page https://asi1.ai/ai/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4 once and wait 1 to 2 minutes for the card. Collapse the ASI:One sidebar so your name and other chats are out of frame. Page zoom 120%. Hold on the question and card header, then scroll gently so row 1 (Kurali APMC, Rs 3,650, 281 km, clears Rs 3,458) is centred for the last 6 s. Do not click Plan this load. Numbers are from the live reply at 22:56 on 24 Oct 2026 and will differ on a new run.
- **Narration:** This is Mandi Net-Price Desk, an agent in ASI one. You write one sentence. It reads the crop, the place and the quantity, pulls today's real mandi prices, and finds real road distances to each one. Then it ranks the mandis by what you actually clear per quintal. Kurali wins, with three thousand four hundred and fifty eight.

## Scene 4: Why the order is what it is: card rows 1 to 3

- **URL or command:** `https://asi1.ai/chat/50a184bf-3b9c-4a31-a2ca-e8218ce5b898`
- **Actions:** Same chat, zoom 120%. Row 1 for about 12 s, scroll to row 2 (Kharar, 3,000, 287 km, clears 2,826), then to row 3 (Farukh Nagar, 2,600, 23 km, clears 2,538), then back to row 1 for the last sentence.
- **Narration:** Kurali pays three thousand six hundred and fifty, and is two hundred and eighty one kilometres away. After distance, transit loss and fees, you clear three thousand four hundred and fifty eight. Kharar pays three thousand and clears two thousand eight hundred and twenty six. The nearest mandi, Farukh Nagar, is only twenty three kilometres away, but pays two thousand six hundred and clears two thousand five hundred and thirty eight. Here a far mandi still wins, because its price is high enough to cover the drive.

## Scene 5: What it is worth: recommendation line

- **URL or command:** `.venv\Scripts\python.exe -u -m mandi.chat_test "I have 25 tonnes of tomato in Gurugram. Where should I sell today?"`
- **Actions:** Windows Terminal, font about 20 pt, dark theme, cls first, directory C:\dev\fetchathon-3. Record the full run (about 55 s), speed the wait up 8x with the on-screen label "local test client, same agent, sped up 8x", then hold on the finished answer. The line "For 250 quintals, picking Kurali APMC over the last option shown is a difference of about Rs 348,196" must be on screen when it is read. ASI:One shows only the card, not this text, so the terminal is used here.
- **Narration:** For this load, picking the best mandi over the last one shown is worth about three hundred and forty eight thousand rupees. That compares the ranked options. It is not a forecast.

## Scene 6: Buyers too: onion for a restaurant in Delhi

- **URL or command:** `.venv\Scripts\python.exe -u -m mandi.chat_test "I run a restaurant in Delhi. Where is onion cheapest to buy today?"`
- **Actions:** Same terminal. Full run about 90 s, sped up 8x with the label, then hold on the answer: Sadhaura APMC first, price 2,200, ~199 km (tilde), landed Rs 2,268.
- **Narration:** It works the other way too. A restaurant in Delhi asks where onion is cheapest to buy. This is our local test client, talking to the same agent. It ranks by landed cost, what you pay including freight and transit loss. Sadhaura comes first, at two thousand two hundred and sixty eight rupees a quintal. A tilde marks a distance that is approximate, because only the district could be located.

## Scene 7: Three agents: architecture image, then Agentverse profiles

- **URL or command:** `https://github.com/TheRealLaksh/fetchathon-3-agent/blob/main/README.md (How it works) ; https://agentverse.ai/agents/details/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4/profile ; https://agentverse.ai/agents/details/agent1qdppp6kky9mlmq9j4c7v0nksqpvusy7w9vjxylzuu6xt48fs20mw7ecwcp0/profile ; https://agentverse.ai/agents/details/agent1qtw0yw8kanxv48wd0v2zrhdg4p6ewersauhstygfy4s2qv20fyxkjl8w9y3/profile`
- **Actions:** README architecture image for the first 4 s, the front agent profile (banner, avatar, @mandi-desk, README badges) for about 9 s, the Price Agent profile 4 s, the Logistics Agent profile 4.5 s, then the architecture image again for the rest. The Agentverse sidebar shows the account email: hide it (or crop it out). The two helper profiles currently show no name or description (only Active and Local).
- **Narration:** Behind that one message are three separate agents on Fetch.ai. The front agent speaks the Agent Chat Protocol through an Agentverse mailbox, and uses the ASI one model only to understand the request. The Price Agent calls the government mandi dataset. The Logistics Agent gets real road routes from OpenStreetMap and OSRM. They pass each other typed messages. The ranking itself is plain code, not model output, so the numbers are repeatable, and nine offline tests check the maths.

## Scene 8: Assumptions you can see and change: SOURCES.md, then an override run

- **URL or command:** `https://github.com/TheRealLaksh/fetchathon-3-agent/blob/main/SOURCES.md ; .venv\Scripts\python.exe -u -m mandi.chat_test "I have 25 tonnes of tomato in Gurugram, my truck costs Rs 4 per tonne-km and my commission agent charges 6%. Where should I sell?"`
- **Actions:** SOURCES.md table for 16 s (freight, market fee, commission, transit loss rows), then the terminal run (about 75 s, sped up 8x with the label) and hold on the footer line: "truck Rs 4 per tonne-km ... agent commission 6% (included)". The live prices had moved since the earlier runs (Sonepat APMC first), so no before and after claim is made.
- **Narration:** Prices, locations and distances are real. Freight, mandi fee and transit loss are assumptions, and the repository lists each one with its source. Commission is left out unless you state it. Tell the agent your own numbers and it uses them: here, a four rupee truck and six percent commission, marked as included. In earlier sensitivity tests, the top of the ranking did not change.

## Scene 9: Reliability: selftest, then the snapshot fallback code

- **URL or command:** `.venv\Scripts\python.exe -m mandi.selftest ; https://github.com/TheRealLaksh/fetchathon-3-agent/blob/main/mandi/core.py#L126`
- **Actions:** Terminal: run the command (finishes in about 3 s, "9 tests passed"), about 5.5 s on screen. Then core.py at line 126, zoom 125%, fetch_prices_with_source in view, scroll about 120 px over the rest of the scene.
- **Narration:** If the government data source is down, the agent answers from the last saved snapshot and says so. If the routing service is down, it estimates distance and marks it approximate. Both fallbacks are covered by the nine tests you just saw, and we tested the price fallback live with a deliberately wrong key.

## Scene 10: Honest limits: README Known limits

- **URL or command:** `https://github.com/TheRealLaksh/fetchathon-3-agent/blob/main/README.md`
- **Actions:** Zoom 125%. Show the Warning box and the bullet list, scroll about 60 px slowly over the scene.
- **Narration:** It still runs on a laptop, the dataset holds only today's prices, and commission is excluded. Next, we host it on Agentverse and keep daily snapshots, so trend advice becomes possible.

## Scene 11: Outro: Agentverse profile, then the repo URL

- **URL or command:** `https://agentverse.ai/agents/details/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4/profile ; https://github.com/TheRealLaksh/fetchathon-3-agent`
- **Actions:** Front agent profile (banner and logo) for about 5.5 s, then the repo page with the URL visible in the address bar.
- **Narration:** Mandi Net-Price Desk. Find it in ASI one as at mandi dash desk, and the code is on GitHub.
