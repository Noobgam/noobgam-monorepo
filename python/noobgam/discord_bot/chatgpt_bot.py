import os
from typing import Dict, List

import discord
from discord import Message

from noobgam.discord_bot.models import UserMessage
from noobgam.discord_bot.openai_utils import respond_to_message_history

CLIENT_ID = 223097750416392192
if os.environ.get("CLIENT_ID_OVERRIDE"):
    CLIENT_ID = int(os.environ["CLIENT_ID_OVERRIDE"])


message_history: Dict[str, List[UserMessage]] = {}
MESSAGE_CAP = 200


def append_message(message: Message):
    id = str(message.guild.id) + "_" + str(message.channel.id)
    l = message_history.get(id, [])
    l.append(UserMessage.from_message(message))
    message_history[id] = l[-MESSAGE_CAP:]


async def reply_message(message: Message):
    id = str(message.guild.id) + "_" + str(message.channel.id)
    l = message_history.get(id, [])
    res = respond_to_message_history(l + [UserMessage.from_message(message)])
    await message.channel.send(res)
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
        # Don't respond to ourselves
        if message.author == client.user:
            append_message(message)
            return

        # Respond to "ping" with "pong"
        print(message.content)
        if message.reference and message.reference.cached_message:
            if message.reference.cached_message.author.id == CLIENT_ID:
                await reply_message(message)
                append_message(message)
                return

        if message.mentions and next(
            (mention for mention in message.mentions if mention.id == CLIENT_ID), None
        ):
            await reply_message(message)
            append_message(message)
            return

        append_message(message)

    client.run(os.environ["DISCORD_PERSONAL_TOKEN"])


if __name__ == "__main__":
    run_bot()
