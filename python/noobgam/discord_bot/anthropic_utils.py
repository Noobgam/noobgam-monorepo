import os
from typing import List

from langchain_community.chat_models import ChatAnthropic
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionUserMessageParam

from noobgam.discord_bot.constants import MODEL_NAME
from noobgam.discord_bot.message_utils import filter_messages
from noobgam.discord_bot.models import UserMessage

client = ChatAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


async def respond_to_message_history(messages: List[UserMessage]) -> str:
    raise NotImplementedError("Not implemented yet")
    messages = filter_messages(messages)
    ATTACH_IMAGES_COMMAND = "/images"
    last_msg = messages[-1].msg
    include_images = ATTACH_IMAGES_COMMAND in last_msg

    images_explanation = (
        "Pictures can be in any of the messages mentioned previously"
        if include_images
        else f"""
        If user requests you to take a look at picture advice them to use {ATTACH_IMAGES_COMMAND}, if this text is not present the images are redacted.
        """
    )

    pre_prompt = f"""
    You are participating in the chat under the name of `{MODEL_NAME}`
    
    You should reply as if you were one of the participants in chat named "{MODEL_NAME}".

    You will be given a list of chat messages one by one, potentially with attachments.
    
    {images_explanation}
    
    Respond only with the text that you would have responded with, do not add anything additional.
    You must not add your name, only add the text response.
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

    response = await client.chat.completions.create(
        model="gpt-4-vision-preview" if include_images else "gpt-4-1106-preview",
        messages=messages,
        max_tokens=2000,
        temperature=0.6,
    )
    return response.choices[0].message.content
