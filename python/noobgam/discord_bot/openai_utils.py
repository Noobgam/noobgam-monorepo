import os
from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

from noobgam.discord_bot.models import UserMessage

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"], organization=os.environ["OPENAI_ORGANIZATION"]
)


def to_openai_message(
    message: UserMessage, include_images: bool = False
) -> ChatCompletionUserMessageParam:
    content = [
        {
            "type": "text",
            "text": f"[{message.username}]: {message.msg} <{len(message.attachment_urls)} images attached>",
        },
    ]
    if include_images and message.attachment_urls:
        for attached_url in message.attachment_urls:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": attached_url, "detail": "high"},
                }
            )
    return {"role": "user", "content": content}


def respond_to_message_history(messages: List[UserMessage]) -> str:
    ATTACH_IMAGES_COMMAND = "/images"

    pre_prompt = f"""
    You are participating in the chat under the name of `Noobgam Bot`
    
    You should reply as if you were one of the participants in chat named "Noobgam Bot".
    Respond only with the text that you would have responded with, do not add anything additional.
    
    You will be given a list of chat messages one by one, potentially with attachments, you can answer as usual.
    
    If the last message does not contain the command "{ATTACH_IMAGES_COMMAND}", you will not get any attachments, tell that to other debate participants if they want you to do something with images.
    """
    last_msg = messages[-1].msg
    include_images = ATTACH_IMAGES_COMMAND in last_msg

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": [{"type": "text", "text": pre_prompt}]},
        ]
        + [
            to_openai_message(message, include_images=include_images)
            for message in messages
        ],
        max_tokens=2000,
    )
    return response.choices[0].message.content
