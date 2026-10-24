"""Chat-protocol test client for the front agent (acts like ASI:One would).

Start price_agent, logistics_agent and front_agent (without USE_MAILBOX) first, then:
    python -m mandi.chat_test "I have 8 tonnes of tomato in Gurugram. Where should I sell today?"
"""
import json
import os
import sys
from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
from uagents import Agent, Context
from uagents.crypto import Identity
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    MetadataContent,
    TextContent,
)

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
        if isinstance(c, MetadataContent) and c.metadata.get("requires_card_interaction") == "true":
            items = json.loads(c.metadata["card_payload"])["root"]["children"][0]["items"]
            print(f"\n[card] kind={c.metadata['card_kind']} items={len(items)}", flush=True)
            tap = os.environ.get("TAP")  # TAP=2 taps "Plan this load" on the 2nd card item, like a user would
            if tap:
                button = [x for x in items[int(tap) - 1]["children"] if x["type"] == "button"][0]
                text = json.dumps(button["action"]["selection"])
                await ctx.send(sender, ChatMessage(timestamp=datetime.now(timezone.utc), msg_id=uuid4(),
                                                   content=[TextContent(type="text", text=text)]))
            else:
                os._exit(0)
        if isinstance(c, EndSessionContent):
            os._exit(0)


if __name__ == "__main__":
    client.run()
