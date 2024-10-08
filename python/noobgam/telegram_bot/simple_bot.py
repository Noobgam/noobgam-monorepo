import asyncio
import base64
import os
from typing import Dict, List

from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from noobgam.discord_bot.constants import MODEL_NAME
from noobgam.discord_bot.models import UserMessage
from noobgam.discord_bot.openai_utils import respond_to_message_history_openai

token = os.environ["TELEGRAM_PERSONAL_TOKEN"]
psw = os.environ["TELEGRAM_PERSONAL_PASSWORD"]

allowlisted_uids = set()
msg_hist: Dict[int, List[UserMessage]] = {}
models_selected: Dict[int, str]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Welcome"
    uid = update.message.chat.id
    if uid not in allowlisted_uids:
        msg += "\nEnter password to continue, none of the messages are persisted"
    await update.message.reply_text(msg)
    msg_hist[uid] = []
    pass


async def generate_image_impl(update: Update, prompt: str):
    if not prompt:
        await update.message.reply_text(
            "Please provide a prompt for the image generation, e.g., /generate_image a white siamese cat")
        return
    await update.message.reply_text(f"Generating image for prompt: [{prompt}], please wait")
    client = AsyncOpenAI(
        api_key=os.environ["OPENAI_API_KEY"], organization=os.environ["OPENAI_ORGANIZATION"]
    )
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )

        # Retrieve image URL
        image_url = (await response).data[0].url

        # Send image URL to user
        await update.message.reply_text(f"Here is your generated image: {image_url}")
    except Exception as e:
        # Handle any errors
        await update.message.reply_text(f"An error occurred: {e}")


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.chat.id
    allowed = uid in allowlisted_uids
    if not allowed:
        if update.message.text and (psw in update.message.text):
            await update.message.reply_text("Password acknowledged")
            allowlisted_uids.add(uid)
            msg_hist[uid] = []
            return
    if not allowed:
        await update.message.reply_text("Enter password to continue")
        return

    if not context.args:
        await update.message.reply_text(
            "Please provide a prompt for the image generation, e.g., /generate_image a white siamese cat")
        return

    # Join all the args to form the prompt
    prompt = " ".join(context.args)
    return await generate_image_impl(update, prompt)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.chat.id
    allowed = uid in allowlisted_uids
    if not allowed:
        if update.message.text and (psw in update.message.text):
            await update.message.reply_text("Password acknowledged")
            allowlisted_uids.add(uid)
            msg_hist[uid] = []
            return
    if not allowed:
        await update.message.reply_text("Enter password to continue")
        return
    if update.message.text and update.message.text.startswith("/generate_image"):
        return await generate_image_impl(update, update.message.text[len("/generate_image") + 1:])

    model_selected = models_selected[uid] or "gpt-4o-2024-08-06"

    if update.message.text and update.message.text.startswith("/get_model"):
        return await update.message.reply_text(model_selected)

    if update.message.text and update.message.text.startswith("/set_model"):
        models_selected[uid] = (update.message.text[len("/set_model") + 1:]).strip()
        return await update.message.reply_text(f"Model set to {models_selected[uid]}")

    photos = update.message.photo or []
    image_attachments: List[str] = []
    if photos:
        file_id = photos[-1].file_id
        new_file = await context.bot.get_file(file_id)
        in_memory_img = await new_file.download_as_bytearray()
        image_attachments.append(base64.b64encode(in_memory_img).decode("utf-8"))
    msg_hist[uid].append(
        UserMessage(
            username=update.message.chat.username or update.message.chat.first_name,
            msg=update.message.caption or update.message.text,
            attachment_urls=[],
            image_attachments=[],
            base64_images=image_attachments,
        )
    )
    response = await respond_to_message_history_openai(msg_hist[uid], model_selected)
    msg_hist[uid].append(
        UserMessage(
            username=MODEL_NAME,
            msg=response,
            attachment_urls=[],
            image_attachments=[],
            base64_images=[],
        )
    )
    print(f"Responding with {response}")
    await update.message.reply_markdown(response)


def run_tg_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = Application.builder().token(os.environ["TELEGRAM_PERSONAL_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("generate_image", generate_image, has_args=1))
    app.add_handler(CommandHandler("get_model", handle_message, has_args=1))
    app.add_handler(CommandHandler("set_model", handle_message, has_args=1))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("Polling")
    app.run_polling(poll_interval=3)
