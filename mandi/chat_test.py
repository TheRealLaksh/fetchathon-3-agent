"""Chat-protocol test client for the front agent (acts like ASI:One would).

Start price_agent, logistics_agent and front_agent (without USE_MAILBOX) first, then:
    python -m mandi.chat_test "I have 8 tonnes of tomato in Gurugram. Where should I sell today?"
"""
import os
import sys
from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
from uagents import Agent, Context
from uagents.crypto import Identity
from uagents_core.contrib.protocols.chat import ChatAcknowledgement, ChatMessage, EndSessionContent, TextContent

load_dotenv()
FRONT = Identity.from_seed(os.environ["AGENT_SEED_PHRASE"], 0).address
QUESTION = " ".join(sys.argv[1:]) or "I have 8 tonnes of tomato in Gurugram. Where should I sell today?"

client = Agent(name="mandi-chat-client", seed=os.environ["AGENT_SEED_PHRASE"] + "-chatclient", port=8005,
               endpoint=["http://127.0.0.1:8005/submit"])
_asked: list = []


@client.on_interval(period=3.0)
async def ask(ctx: Context):
    if _asked:
        return
    _asked.append(True)
    await ctx.send(FRONT, ChatMessage(timestamp=datetime.now(timezone.utc), msg_id=uuid4(),
                                      content=[TextContent(type="text", text=QUESTION)]))


@client.on_message(ChatAcknowledgement)
async def ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    print("(ack)", flush=True)


@client.on_message(ChatMessage)
async def reply(ctx: Context, sender: str, msg: ChatMessage):
    for c in msg.content:
        if isinstance(c, TextContent):
            print("\n" + c.text, flush=True)
        if isinstance(c, EndSessionContent):
            os._exit(0)


if __name__ == "__main__":
    client.run()
