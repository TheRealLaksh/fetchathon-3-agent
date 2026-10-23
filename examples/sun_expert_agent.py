"""Starter template: an ASI:One-compatible chat agent (the docs' "Sun expert").

Verified locally on 2026-10-23: a client agent sent a ChatMessage, this agent
acknowledged it, called the ASI1 LLM and replied. Copy this file to start the real agent.

Run:   python examples/sun_expert_agent.py
For ASI:One chat set USE_MAILBOX=1, then open the Inspector link it prints,
click Connect, then Mailbox (needs an Agentverse login).
"""
import os

from dotenv import load_dotenv
from openai import OpenAI
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

load_dotenv()

SUBJECT = "the sun"
client = OpenAI(base_url="https://api.asi1.ai/v1", api_key=os.environ["ASI1_API_KEY"])

agent = Agent(
    name="ASI-agent",
    seed=os.environ["AGENT_SEED_PHRASE"],
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
    mailbox=os.environ.get("USE_MAILBOX") == "1",
    publish_agent_details=True,
)
protocol = Protocol(spec=chat_protocol_spec)


@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Always acknowledge first, then do the work.
    await ctx.send(sender, ChatAcknowledgement(acknowledged_msg_id=msg.msg_id))
    text = "".join(i.text for i in msg.content if isinstance(i, TextContent))
    response = "Sorry, something went wrong on my side. Please try again."
    try:
        r = client.chat.completions.create(
            model="asi1",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant who only answers questions about {SUBJECT}. "
                    "If the user asks about anything else, politely say you do not know.",
                },
                {"role": "user", "content": text},
            ],
            max_tokens=2048,
        )
        response = str(r.choices[0].message.content)
    except Exception as err:  # keep the chat alive if the LLM call fails
        ctx.logger.exception("Error querying model: %s", err)
    await ctx.send(
        sender,
        ChatMessage(content=[TextContent(type="text", text=response), EndSessionContent(type="end-session")]),
    )


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


# publish_manifest=True lets Agentverse and ASI:One see that this agent speaks the chat protocol.
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
