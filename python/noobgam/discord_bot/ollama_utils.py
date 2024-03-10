import asyncio
import json
from typing import List

import requests

from noobgam.discord_bot.constants import MODEL_NAME
from noobgam.discord_bot.message_utils import filter_messages
from noobgam.discord_bot.models import UserMessage


async def ollama_respond_to_message_history(messages: List[UserMessage]) -> str:
    def impl():
        nonlocal messages
        # very expensive, just to test for now.
        messages = filter_messages(messages[-5:])

        raw_messages = [f"[{message.username}]: {message.msg}" for message in messages]

        message_history = "\n".join(raw_messages)

        full_prompt = f"""You are {MODEL_NAME} and you are participating in a chat. Try to stay based, misogynistic and funny. Keep in character.
        You will get a chat history, and should respond only with the message content. Do not prepend your name, do not try speak for other people.

        Current message history:
{message_history}
        """

        res = requests.post(
            "http://127.0.0.1:11434/api/generate",
            data=json.dumps(
                {
                    "model": "dolphin-mixtral:latest",
                    "prompt": full_prompt,
                    "stream": False,
                }
            ),
        )
        return res.json()["response"]

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, impl)
