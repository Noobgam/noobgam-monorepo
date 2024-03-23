import asyncio
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from typing import Dict, List

from noobgam.discord_bot.constants import MODEL_NAME
from noobgam.discord_bot.models import UserMessage
from noobgam.discord_bot.openai_utils import respond_to_message_history

token = os.environ["TELEGRAM_PERSONAL_TOKEN"]
psw = os.environ["TELEGRAM_PERSONAL_PASSWORD"]

allowlisted_uids = set()
msg_hist: Dict[int, List[UserMessage]] = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Welcome"
    uid = update.message.chat.id
    if uid not in allowlisted_uids:
        msg += "\nEnter password to continue, none of the messages are persisted"
    await update.message.reply_text(msg)
    msg_hist[uid] = []
    pass


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.message.chat.id
    allowed = uid in allowlisted_uids
    if not allowed and psw in text:
        await update.message.reply_text("Password acknowledged")
        allowlisted_uids.add(uid)
        msg_hist[uid] = []
    elif not allowed:
        await update.message.reply_text("Enter password to continue")
    else:
        msg_hist[uid].append(
            UserMessage(
                username=update.message.chat.username or update.message.chat.first_name,
                msg=update.message.text or "",
                attachment_urls=[],
            )
        )
        response = await respond_to_message_history(msg_hist[uid])
        msg_hist[uid].append(
            UserMessage(
                username=MODEL_NAME,
                msg=response,
                attachment_urls=[],
            )
        )
        print(f"Responding with {response}")
        await update.message.reply_markdown(response)


def run_tg_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = Application.builder().token(os.environ["TELEGRAM_PERSONAL_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Polling")
    app.run_polling(poll_interval=3)
