![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

# Mandi Net-Price Desk

Tell me what you have or need, and where you are. I rank real Indian mandis by what you actually clear after real road freight, transit loss and mandi fees, using today's government prices. Sellers get the best net price, buyers get the cheapest landed cost.

**Try:**
- I have 25 tonnes of tomato in Gurugram. Where should I sell today?
- I run a restaurant in Delhi. Where is onion cheapest to buy today?
- I have 5 tonnes of potato in Gurugram. Where do I sell?

**How it works:** this agent reads your request with the ASI1 model, then asks two helper agents: the Mandi Price Agent (today's modal prices from data.gov.in) and the Mandi Logistics Agent (road distance and drive time from OpenStreetMap and OSRM). The ranking is plain code, not model output. Every reply lists the assumptions it used (freight, mandi fee, agent commission, transit loss) and you can override them, for example "my truck costs Rs 4 per tonne-km".

**Good to know:** prices are a daily snapshot, not a forecast. Agent commission is not included unless you state it. Replies can take a minute or two because live data is fetched.

Agent address: agent1qv7jdg7dyduuns3n4sp04gu5jkdhxv2s803p824h9c37ymw64mj7ufy86n4

Code, sources and tests: https://github.com/TheRealLaksh/fetchathon-3-agent

Built at Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union Gurugram). Team fetchathon3.0-5865: Laksh Pradhwani, Mark Patel, Aryan Rao, Saiansh Kathuria.
