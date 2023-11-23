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
    last_msg = messages[-1].msg
    include_images = ATTACH_IMAGES_COMMAND in last_msg

    images_explanation = (
        "Pictures can be in any of the messages mentioned previously"
        if include_images
        else f"""
        If user requests you to take a look at picture advice them to use {ATTACH_IMAGES_COMMAND}, other agent will respond from the name of NoobGPT.
        """
    )

    pre_prompt = f"""
    You are participating in the chat under the name of `NoobGPT`
    
    You should reply as if you were one of the participants in chat named "NoobGPT".
    
    You will be given a list of chat messages one by one, potentially with attachments, you can answer as usual.
    
    {images_explanation}
    
    Respond only with the text that you would have responded with, do not add anything additional.
    You do not need to add the tags with your name or the number of attachments, only the text response.
    """

    messages = [
        {"role": "system", "content": [{"type": "text", "text": pre_prompt}]},
    ] + [
        to_openai_message(message, include_images=include_images)
        for message in messages
    ]
    if include_images:
        # there's a 10k token per minute limit, that's very limiting for 200 messages.
        messages = [messages[0]] + messages[1:][-20:]

    response = client.chat.completions.create(
        model="gpt-4-vision-preview" if include_images else "gpt-4-1106-preview",
        messages=messages,
        max_tokens=2000,
    )
    return response.choices[0].message.content
