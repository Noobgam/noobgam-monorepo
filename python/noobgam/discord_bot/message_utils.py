from typing import List

from noobgam.discord_bot.models import UserMessage


def filter_messages(messages: List[UserMessage]) -> List[UserMessage]:
    i = 0
    while i < len(messages):
        if "/clear" in messages[i].msg:
            messages = messages[i + 1 :]
            i = 0
            continue
        i += 1
    return messages
