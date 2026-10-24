# Demo video script (target 4 minutes, limit 3 to 5)

Record the screen with voice-over. ASI:One takes 1 to 2 minutes to pass a message to the agent and the chat page needs a reload, so **ask the question before you start recording**, then show the finished chat. Cut or speed up any waiting. Do not pretend it is instant.

## Before recording (10 minutes)

- All three processes running (`price_agent`, `logistics_agent`, `front_agent` with `USE_MAILBOX=1`), laptop plugged in and awake.
- Cache warm for the demo crops (`python -m mandi.warm_cache Tomato Onion Potato -- "Gurugram, Haryana" "Delhi, NCT of Delhi"`), run while no question is being answered.
- Two ASI:One chats already answered: the tomato seller question (with the card) and the onion buyer question (Delhi). Keep them open in tabs.
- Tabs ready: GitHub repo, Agentverse profile, `SOURCES.md` on GitHub, a terminal in the repo.
- Do not restart the agents once the chats are done.

## Scenes

**0:00 to 0:25, the problem** (show the Agentverse banner or the README title)
> "A trader in Gurugram has 25 tonnes of tomatoes. The government publishes the price at every mandi, but the highest price is not the best deal. You still pay for the drive, lose some produce on the road, and pay mandi fees. Mandi Net-Price Desk does that maths for you, from one sentence in ASI:One."

**0:25 to 1:20, the demo** (ASI:One, the answered tomato chat)
> "I ask: I have 25 tonnes of tomato in Gurugram, where should I sell today? The agent reads the crop, place and quantity, pulls today's real prices, and gets real road distances."

Scroll the table. Point at three rows.
> "Sohna, Gohana and Narnaul all pay Rs 2,500 a quintal. After distance, transit loss and fees they clear Rs 2,443, 2,411 and 2,407. Patiala pays Rs 2,400 and clears Rs 2,254. The reply also tells me what the choice is worth for my quantity, and lists every assumption it used."

Show the interactive card.
> "The top mandis also come as an interactive card in ASI:One."

**1:20 to 1:50, buyer mode** (onion chat, Delhi restaurant)
> "It works the other way too. A restaurant in Delhi asks where onion is cheapest to buy. The agent ranks by landed cost, what you pay including freight and transit loss, not by sticker price."

**1:50 to 2:50, how it is built** (README diagram, then the agent table)
> "Behind one chat message are three separate agents. The front agent speaks the Agent Chat Protocol, uses the ASI1 model only to understand the request, and orchestrates. The Price Agent calls the government daily mandi dataset. The Logistics Agent gets real road routes from OpenStreetMap and OSRM. The agents send each other typed messages, and the ranking itself is plain code, so the numbers are repeatable, with nine offline tests."

Show `mandi/models.py` briefly, then run `python -m mandi.selftest` and let the nine "ok" lines show.

**2:50 to 3:35, honesty and fallbacks** (SOURCES.md, then the terminal or a saved fallback reply)
> "Prices, locations and distances are real. Freight, mandi fee and transit loss are assumptions, shown in every reply and sourced in this file, and you can override them in chat. Commission is left out unless you state it, because I could not find one reliable rate. If the government API is down, the agent answers from the last saved snapshot and says so. I tested that with a wrong API key."

Show the line "Live government prices were unreachable, so this uses the last saved snapshot" if you have a saved reply.

**3:35 to 4:00, close** (repo page)
> "It is live in ASI:One as the Mandi Net-Price Desk. The repo, the Agentverse profiles and this chat are linked in the submission. Known limits: it runs on a laptop for now, and there is no price history in the dataset, so no wait-and-sell advice yet. Thank you."

## Do not say

- Do not call the card button a working feature: the "Plan this load" tap is not confirmed inside ASI:One.
- Do not claim real users or savings figures. Use only the real example above.
- Do not say it is instant. Say the demo chat was asked in advance.
