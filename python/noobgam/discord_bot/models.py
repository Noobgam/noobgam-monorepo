from dataclasses import dataclass
from typing import List

from discord import Attachment, Message


@dataclass
class UserMessage:
    username: str
    msg: str
    # list of urls to pictures
    attachment_urls: List[str]
    image_attachments: List[Attachment]

    @staticmethod
    def from_message(message: Message):
        return UserMessage(
            username=str(message.author.name),
            msg=str(message.clean_content),
            attachment_urls=[
                attachment.url
                for attachment in message.attachments
                if attachment.content_type
                and attachment.content_type.startswith("image")
            ],
            image_attachments=[
                attachment
                for attachment in message.attachments
                if attachment.content_type
                and attachment.content_type.startswith("image")
            ],
        )
