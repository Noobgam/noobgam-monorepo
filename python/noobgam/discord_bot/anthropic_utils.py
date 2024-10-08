import base64
from typing import List

import anthropic
import httpx

from noobgam.discord_bot.message_utils import filter_messages
from noobgam.discord_bot.models import UserMessage
from noobgam.discord_bot.prompt_templates import PRE_CHAT_PROMPT

client = anthropic.Anthropic()


def url_to_base64_image(url: str) -> str:
    return base64.b64encode(httpx.get(url).content).decode("utf-8")


def to_anthropic_message_contents(message: UserMessage, include_images: bool = False):
    first_text = f"[{message.username}]: {message.msg}"
    if len(message.attachment_urls):
        first_text += f"<{len(message.attachment_urls)} images attached>"
    contents = [{"type": "text", "text": first_text}]
    if include_images and message.attachment_urls:
        for attached_image in message.image_attachments:
            contents.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": attached_image.content_type,
                        "data": url_to_base64_image(attached_image.url),
                    },
                }
            )
        for image_base64 in message.base64_images:
            contents.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_base64,
                    },
                }
            )
    return contents


async def respond_to_message_history_claude(messages: List[UserMessage], model_id) -> str:
    messages = filter_messages(messages)
    include_images = True

    pre_prompt = PRE_CHAT_PROMPT

    contents = [
        to_anthropic_message_contents(message, include_images=include_images)
        for message in messages
    ]

    def flatten(nested_list):
        return [item for sublist in nested_list for item in sublist]

    contents = flatten(contents)
    new_resp = client.messages.create(
        model=model_id,
        max_tokens=2500,
        temperature=0.3,
        system=pre_prompt,
        messages=[{"role": "user", "content": contents}],
    )
    return new_resp.content[0].text
