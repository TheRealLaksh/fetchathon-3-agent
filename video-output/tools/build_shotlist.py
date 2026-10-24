"""Writes shotlist.md from the narration files. Run from video-output."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
N = lambda n: open(f"narration/scene{n}.txt", encoding="utf-8").read().strip()

REPO = "https://github.com/TheRealLaksh/fetchathon-3-agent"
FRONT = "https://agentverse.ai/agents/details/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4/profile"
PRICE = "https://agentverse.ai/agents/details/agent1qdppp6kky9mlmq9j4c7v0nksqpvusy7w9vjxylzuu6xt48fs20mw7ecwcp0/profile"
LOGI = "https://agentverse.ai/agents/details/agent1qtw0yw8kanxv48wd0v2zrhdg4p6ewersauhstygfy4s2qv20fyxkjl8w9y3/profile"
CHAT = "https://asi1.ai/chat/50a184bf-3b9c-4a31-a2ca-e8218ce5b898"

scenes = [
 ("01", "Hook: README hero, then the example answer image", REPO + "/blob/main/README.md",
  "Browser zoom 125%. Start at the README top (banner, tagline, badges). After about 8 s scroll slowly down to the \"What an answer looks like\" image and stop with rows 1 to 3 in view. The image is the 8-tonne example from the README, not today's live answer, so the narration says \"in this example run\"."),
 ("02", "The problem: README at-a-glance block", REPO + "/blob/main/README.md",
  "Browser zoom 125%. Show the badge row and the three-column block (The problem / What it does / What is different); scroll down by about 80 px over the whole scene."),
 ("03", "Ask in ASI:One: the live tomato chat", CHAT + "  (after sending: @agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4 I have 25 tonnes of tomato in Gurugram. Where should I sell today?)",
  "Send the question from the agent profile page https://asi1.ai/ai/agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4 once and wait 1 to 2 minutes for the card. Collapse the ASI:One sidebar so your name and other chats are out of frame. Page zoom 120%. Hold on the question and card header, then scroll gently so row 1 (Kurali APMC, Rs 3,650, 281 km, clears Rs 3,458) is centred for the last 6 s. Do not click Plan this load. Numbers are from the live reply at 22:56 on 24 Oct 2026 and will differ on a new run."),
 ("04", "Why the order is what it is: card rows 1 to 3", CHAT,
  "Same chat, zoom 120%. Row 1 for about 12 s, scroll to row 2 (Kharar, 3,000, 287 km, clears 2,826), then to row 3 (Farukh Nagar, 2,600, 23 km, clears 2,538), then back to row 1 for the last sentence."),
 ("05", "What it is worth: recommendation line", ".venv\\Scripts\\python.exe -u -m mandi.chat_test \"I have 25 tonnes of tomato in Gurugram. Where should I sell today?\"",
  "Windows Terminal, font about 20 pt, dark theme, cls first, directory C:\\dev\\fetchathon-3. Record the full run (about 55 s), speed the wait up 8x with the on-screen label \"local test client, same agent, sped up 8x\", then hold on the finished answer. The line \"For 250 quintals, picking Kurali APMC over the last option shown is a difference of about Rs 348,196\" must be on screen when it is read. ASI:One shows only the card, not this text, so the terminal is used here."),
 ("06", "Buyers too: onion for a restaurant in Delhi", ".venv\\Scripts\\python.exe -u -m mandi.chat_test \"I run a restaurant in Delhi. Where is onion cheapest to buy today?\"",
  "Same terminal. Full run about 90 s, sped up 8x with the label, then hold on the answer: Sadhaura APMC first, price 2,200, ~199 km (tilde), landed Rs 2,268."),
 ("07", "Three agents: architecture image, then Agentverse profiles", REPO + "/blob/main/README.md (How it works) ; " + FRONT + " ; " + PRICE + " ; " + LOGI,
  "README architecture image for the first 4 s, the front agent profile (banner, avatar, @mandi-desk, README badges) for about 9 s, the Price Agent profile 4 s, the Logistics Agent profile 4.5 s, then the architecture image again for the rest. The Agentverse sidebar shows the account email: hide it (or crop it out). The two helper profiles currently show no name or description (only Active and Local)."),
 ("08", "Assumptions you can see and change: SOURCES.md, then an override run", REPO + "/blob/main/SOURCES.md ; .venv\\Scripts\\python.exe -u -m mandi.chat_test \"I have 25 tonnes of tomato in Gurugram, my truck costs Rs 4 per tonne-km and my commission agent charges 6%. Where should I sell?\"",
  "SOURCES.md table for 16 s (freight, market fee, commission, transit loss rows), then the terminal run (about 75 s, sped up 8x with the label) and hold on the footer line: \"truck Rs 4 per tonne-km ... agent commission 6% (included)\". The live prices had moved since the earlier runs (Sonepat APMC first), so no before and after claim is made."),
 ("09", "Reliability: selftest, then the snapshot fallback code", ".venv\\Scripts\\python.exe -m mandi.selftest ; " + REPO + "/blob/main/mandi/core.py#L126",
  "Terminal: run the command (finishes in about 3 s, \"9 tests passed\"), about 5.5 s on screen. Then core.py at line 126, zoom 125%, fetch_prices_with_source in view, scroll about 120 px over the rest of the scene."),
 ("10", "Honest limits: README Known limits", REPO + "/blob/main/README.md",
  "Zoom 125%. Show the Warning box and the bullet list, scroll about 60 px slowly over the scene."),
 ("11", "Outro: Agentverse profile, then the repo URL", FRONT + " ; " + REPO,
  "Front agent profile (banner and logo) for about 5.5 s, then the repo page with the URL visible in the address bar."),
]

out = ["# Shot list: Mandi Net-Price Desk demo (screen recording)\n",
       "Recorded 24 to 25 Oct 2026. Capture: ffmpeg gdigrab 2560x1440 from the top-left of a 2560x1600 display, scaled to 1920x1080, 30 fps. Brave window with only Claude's tab group (bookmarks bar hidden), terminal = Windows Terminal. Narration: Windows \"Microsoft Zira Desktop\" voice, one WAV per scene in `audio/`, played 1.04x in the final cut.\n",
       "Live numbers change through the day (data.gov.in): scenes 3, 4, 5, 6 and 8 narrate only what was on screen at the time of recording. Re-record those scenes and rewrite their text from the new screen if you redo them.\n",
       "Speed-ups: the terminal waits in scenes 5, 6 and 8 are sped up 8x and labelled on screen. Nothing else is sped up (apart from the global 1.04x).\n"]
for n, title, where, how in scenes:
    out.append(f"## Scene {int(n)}: {title}\n\n- **URL or command:** `{where}`\n- **Actions:** {how}\n- **Narration:** {N(n)}\n")
open("shotlist.md", "w", encoding="utf-8").write("\n".join(out))
print("shotlist.md written")
