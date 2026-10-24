![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

# Mandi Weather Agent

Helper agent of the Mandi Net-Price Desk (front agent `@mandi-desk`).

**What it does:** receives a `WeatherRequest` (a list of places) and replies with a `WeatherReply`: today's real maximum and minimum temperature and rain chance for each place, from Open-Meteo (free service, no key). The front agent asks for the trader's place and the top-ranked mandis' districts, and shows the numbers next to the ranking. The weather does not change the ranking maths: the transit-loss assumption stays a fixed, stated assumption.

It is called by the front agent, not by end users. To use the service, ask the front agent in ASI:One.

Agent address: agent1qdwntp8eujpl5cs5a808ygnyaedpdj4dvdlt9pc0qqwwwcshrcxcygjsvnt

Code, sources and tests: https://github.com/TheRealLaksh/fetchathon-3-agent

Built at Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union Gurugram). Team fetchathon3.0-5865.
