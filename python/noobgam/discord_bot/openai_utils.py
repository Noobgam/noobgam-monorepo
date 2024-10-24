import os
from typing import List

import httpx
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
    if len(message.image_attachments):
        first_text += f"<{len(message.image_attachments)} images attached>"
    content = [{"type": "text", "text": first_text}]
    if include_images:
        for attached in message.image_attachments:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": attached.url, "detail": "high"},
                }
            )
    for attached in message.text_attachments:
        attachment_content = httpx.get(attached.url).content
        content.append(
            {
                "type": "text",
                "text": f"Attached file: {attached.filename}\n Content:\n{attachment_content}",
            }
        )
    return {"role": "user", "content": content}


async def respond_to_message_history_openai(messages: List[UserMessage], model_id: str) -> str:
    messages = filter_messages(messages)

    pre_prompt = PRE_CHAT_PROMPT

    mapped_messages: List[ChatCompletionUserMessageParam]
    stripped_model = model_id in ["o1-preview", "o1-mini"]

    if stripped_model:
        mapped_messages = [
            {"role": "user", "content": [{"type": "text", "text": pre_prompt}]},
        ] + [
            to_openai_message(message, include_images=False)
            for message in messages
        ]
    else:
        mapped_messages = [
            {"role": "system", "content": [{"type": "text", "text": pre_prompt}]},
        ] + [
            to_openai_message(message, include_images=True)
            for message in messages
        ]

    response = await client.chat.completions.create(
        model=model_id,
        messages=mapped_messages,
        max_completion_tokens=4000,
        temperature=1 if stripped_model else 0.6,
    )
    return response.choices[0].message.content
