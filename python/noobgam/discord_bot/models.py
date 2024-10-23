from dataclasses import dataclass
from typing import List, Optional

from discord import Attachment, Message


@dataclass
class UserMessage:
    username: str
    msg: str
    # list of urls to pictures
    image_attachments: List[Attachment]
    text_attachments: List[Attachment]
    base64_images: Optional[List[str]] = None

    @staticmethod
    def from_message(message: Message):
        return UserMessage(
            username=str(message.author.name),
            msg=str(message.clean_content),
            image_attachments=[
                attachment
                for attachment in message.attachments
                if attachment.content_type
                and attachment.content_type.startswith("image")
            ],
            text_attachments=[
                attachment
                for attachment in message.attachments
                if attachment.content_type
                and attachment.content_type.startswith("text/plain")
            ],
            base64_images=[],
        )
