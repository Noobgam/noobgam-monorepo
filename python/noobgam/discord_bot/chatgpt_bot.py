import os
from typing import Dict, List

import discord
from discord import Message
from discord.abc import Messageable

from noobgam.discord_bot.models import UserMessage
from noobgam.discord_bot.openai_utils import respond_to_message_history

CLIENT_ID = 223097750416392192
if os.environ.get("CLIENT_ID_OVERRIDE"):
    CLIENT_ID = int(os.environ["CLIENT_ID_OVERRIDE"])

message_history: Dict[str, List[UserMessage]] = {}
MESSAGE_CAP = 200
DISCORD_MESSAGE_LENGTH_CAP = 2000


async def get_history_from_channel(message: Message) -> List[UserMessage]:
    key = str(message.guild.id) + "_" + str(message.channel.id)
    result: List[UserMessage] = message_history.get(key, None)
    if not result:
        result = list(
            reversed(
                [
                    UserMessage.from_message(message)
                    async for message in message.channel.history(limit=MESSAGE_CAP)
                ]
            )
        )
    return result


async def append_message(message: Message):
    id = str(message.guild.id) + "_" + str(message.channel.id)
    l = await get_history_from_channel(message)
    l.append(UserMessage.from_message(message))
    message_history[id] = l[-MESSAGE_CAP:]


async def send_message(channel: Messageable, message: str):
    async def send_first_n(n: int):
        nonlocal message

        await channel.send(message[:n])
        message = message[n:]

    while len(message) > DISCORD_MESSAGE_LENGTH_CAP:
        # try to separate the text before code
        lindex = message.find("```")
        if 50 < lindex < DISCORD_MESSAGE_LENGTH_CAP:
            await send_first_n(lindex)
            continue
        rindex = message.find("```", lindex + 3)
        if rindex != -1 and rindex < DISCORD_MESSAGE_LENGTH_CAP:
            await send_first_n(DISCORD_MESSAGE_LENGTH_CAP + 3)
            continue

        await send_first_n(DISCORD_MESSAGE_LENGTH_CAP)
        continue
    await send_first_n(len(message))


async def reply_message(message: Message):
    user_messages = await get_history_from_channel(message)
    async with message.channel.typing():
        res = await respond_to_message_history(user_messages)
        await send_message(message.channel, res)
        return res


def run_bot():
    # Define the intents
    intents = discord.Intents.default()
    intents.messages = True  # If you want to handle messages
    intents.guilds = True  # If you need guild information
    intents.message_content = True  # Ensure this is enabled

    # Create an instance of a Client, which represents a connection to Discord
    client = discord.Client(intents=intents)

    # Register an event to track when the bot has completed logging in
    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    # Register an event to respond to messages
    @client.event
    async def on_message(message: Message):
        await append_message(message)
        # Don't respond to ourselves
        if message.author == client.user:
            return

        # Respond to "ping" with "pong"
        if message.reference and message.reference.cached_message:
            if message.reference.cached_message.author.id == CLIENT_ID:
                await reply_message(message)
                return

        if message.mentions and next(
            (mention for mention in message.mentions if mention.id == CLIENT_ID), None
        ):
            await reply_message(message)
            return

    client.run(os.environ["DISCORD_PERSONAL_TOKEN"])


if __name__ == "__main__":
    run_bot()
