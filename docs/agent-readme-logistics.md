![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

# Mandi Logistics Agent

Helper agent of the Mandi Net-Price Desk (front agent `@mandi-desk`).

**What it does:** receives a `RouteRequest` (an origin and a list of mandis) and replies with a `RouteReply`: real road distance and drive time from the origin to each mandi. It finds each mandi with OpenStreetMap Nominatim (falling back to the district centre, marked approximate) and gets the road route from OSRM. If the routing service is unreachable it estimates distance from straight-line distance and marks it approximate.

It is called by the front agent, not by end users. To use the service, ask the front agent in ASI:One.

Agent address: agent1qtw0yw8kanxv48wd0v2zrhdg4p6ewersauhstygfy4s2qv20fyxkjl8w9y3

Code, sources and tests: https://github.com/TheRealLaksh/fetchathon-3-agent

Built at Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union Gurugram). Team fetchathon3.0-5865.
