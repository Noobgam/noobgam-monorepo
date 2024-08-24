import os
from typing import List

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionUserMessageParam

from noobgam.discord_bot.message_utils import filter_messages
from noobgam.discord_bot.models import UserMessage
from noobgam.discord_bot.prompt_templates import PRE_CHAT_PROMPT

client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"], organization=os.environ["OPENAI_ORGANIZATION"]
)


def to_openai_message(
    message: UserMessage, include_images: bool = False
) -> ChatCompletionUserMessageParam:
    first_text = f"[{message.username}]: {message.msg}"
    if len(message.attachment_urls):
        first_text += f"<{len(message.attachment_urls)} images attached>"
    content = [{"type": "text", "text": first_text}]
    if include_images:
        for attached_url in message.attachment_urls:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": attached_url, "detail": "high"},
                }
            )
        for base64_image in message.base64_images:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                }
            )
    return {"role": "user", "content": content}


async def respond_to_message_history_openai(messages: List[UserMessage]) -> str:
    messages = filter_messages(messages)

    pre_prompt = PRE_CHAT_PROMPT

    messages = [
        {"role": "system", "content": [{"type": "text", "text": pre_prompt}]},
    ] + [
        to_openai_message(message, include_images=True)
        for message in messages
    ]

    response = await client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        max_tokens=4000,
        temperature=0.6,
    )
    return response.choices[0].message.content
