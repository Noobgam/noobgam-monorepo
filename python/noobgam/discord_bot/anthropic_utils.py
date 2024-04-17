import base64
from typing import List

import anthropic
import httpx

from noobgam.discord_bot.constants import MODEL_NAME
from noobgam.discord_bot.message_utils import filter_messages
from noobgam.discord_bot.models import UserMessage

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
    return contents


async def respond_to_message_history_claude(messages: List[UserMessage]) -> str:
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

    contents = [
        to_anthropic_message_contents(message, include_images=include_images)
        for message in messages
    ]
    if include_images:
        # there's a 10k token per minute limit, that's very limiting for 200 messages.
        contents = [contents[0]] + contents[1:][-20:]

    def flatten(nested_list):
        return [item for sublist in nested_list for item in sublist]

    contents = flatten(contents)
    new_resp = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2500,
        temperature=0.0,
        system=pre_prompt,
        messages=[{"role": "user", "content": contents}],
    )
    return new_resp.content[0].text
