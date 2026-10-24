![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

# Mandi Price Agent

Helper agent of the Mandi Net-Price Desk (front agent `@mandi-desk`).

**What it does:** receives a `PriceRequest` (crop, optional states) and replies with a `PriceReply`: today's real modal, minimum and maximum prices per mandi, in rupees per quintal, from the government daily mandi dataset on data.gov.in. If the live API is unreachable it replies from the last saved snapshot and marks the reply as a snapshot with its save time.

It is called by the front agent, not by end users. To use the service, ask the front agent in ASI:One.

Agent address: agent1qdppp6kky9mlmq9j4c7v0nksqpvusy7w9vjxylzuu6xt48fs20mw7ecwcp0

Code, sources and tests: https://github.com/TheRealLaksh/fetchathon-3-agent

Built at Fetch-A-Thon 3.0 (Fetch.ai Innovation Lab x Masters' Union Gurugram). Team fetchathon3.0-5865.
