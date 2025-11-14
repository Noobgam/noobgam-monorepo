import asyncio
import base64
import logging
import os
import pickle
from io import BytesIO
from typing import Dict, List, Literal, Optional
import google.generativeai as genai

from openai import AsyncOpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters, CallbackQueryHandler,
)

from noobgam.discord_bot.constants import MODEL_NAME
from noobgam.discord_bot.models import UserMessage
from noobgam.discord_bot.openai_utils import respond_to_message_history_openai

token = os.environ["TELEGRAM_PERSONAL_TOKEN"]
psw = os.environ["TELEGRAM_PERSONAL_PASSWORD"]

genai.configure(api_key=os.environ["GENAI_API_KEY"])

state = os.environ["STATE_FILE"]

STATE_LOCK = asyncio.Lock()

allowlisted_uids = set()
msg_hist: Dict[int, List[UserMessage]] = {}
models_selected: Dict[int, str] = {}
image_models_selected: Dict[int, str] = {}

# Updated model list to match the reference
AVAILABLE_MODELS = [
    "gpt-4.1",
    "gpt-5.1",
    "sonnet-4.5",
    "opus-4.1",
    "o4-mini-high",
    "gemini-2.5-pro",
]

def restore_state():
    global allowlisted_uids, msg_hist, models_selected, image_models_selected
    if not os.path.exists(state):
        logging.info("No data on startup")
        return
    try:
        with open(state, "rb") as f:
            data = pickle.load(f)
            allowlisted_uids = data.get("allowlisted_uids", set())
            msg_hist = data.get("msg_hist", {})
            models_selected = data.get("models_selected", {})
            image_models_selected = data.get("image_models_selected", {})
        logging.info("State restored from file.")
    except Exception as e:
        logging.info(f"Could not restore state: {e}")


async def write_state():
    async with STATE_LOCK:
        data = {
            "allowlisted_uids": allowlisted_uids,
            "msg_hist": msg_hist,
            "models_selected": models_selected,
            "image_models_selected": image_models_selected,
        }
        try:
            with open(state, "wb") as f:
                pickle.dump(data, f)
            logging.info("State written to file.")
        except Exception as e:
            logging.info(f"Could not write state: {e}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Welcome"
    uid = update.message.chat.id
    if uid not in allowlisted_uids:
        msg += "\nEnter password to continue, none of the messages are persisted"
    await update.message.reply_text(msg)
    msg_hist[uid] = []
    await write_state()


async def generate_image_impl(update: Update, prompt: str):
    if not prompt:
        await update.message.reply_text(
            "Please provide a prompt for the image generation, e.g., /generate_image a white siamese cat")
        return
    await update.message.reply_text(f"Generating image for prompt: [{prompt}], please wait")
    image_model = image_models_selected.get(update.message.chat.id, "dallee")
    if image_model == "dallee":
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
            await write_state()
        except Exception as e:
            # Handle any errors
            await update.message.reply_text(f"An error occurred: {e}")
    else:
        imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

        result = imagen.generate_images(
            prompt=prompt,
            number_of_images=2,
            safety_filter_level="block_only_high",
            person_generation="allow_adult",
            aspect_ratio="1:1",
        )
        for img in result.images:
            await update.message.reply_photo(photo=BytesIO(img._image_bytes))


async def set_model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Show the user a list of models to pick from.
    """
    uid = update.message.chat.id
    if uid not in allowlisted_uids:
        await update.message.reply_text("You are not authorized to use this command. Please enter the password first.")
        return

    keyboard = [
        [InlineKeyboardButton(model, callback_data=f"set_model:{model}")]
        for model in AVAILABLE_MODELS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the model picker
    await update.message.reply_text("Please choose a model:", reply_markup=reply_markup)


async def set_image_model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Show the user a list of models to pick from.
    """
    uid = update.message.chat.id
    if uid not in allowlisted_uids:
        await update.message.reply_text("You are not authorized to use this command. Please enter the password first.")
        return

    # Create an inline keyboard with model options
    keyboard = [
        [InlineKeyboardButton(model, callback_data=f"set_image_model:{model}")]
        for model in ["dallee", "imagen-3.0-generate-001"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the model picker
    await update.message.reply_text("Please choose a model:", reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle button clicks from the inline keyboard.
    """
    query = update.callback_query
    uid = query.message.chat.id

    if uid not in allowlisted_uids:
        await query.answer("Unauthorized. Please enter the password first.")
        return

    # Parse the callback data
    callback_data = query.data
    if callback_data.startswith("set_model:"):
        selected_model = callback_data.split(":", 1)[1]
        models_selected[uid] = selected_model

        await query.answer(f"Model set to {selected_model}")
        await query.edit_message_text(f"Model successfully set to: {selected_model}")
        await write_state()
    elif callback_data.startswith("set_image_model:"):
        selected_model = callback_data.split(":", 1)[1]
        image_models_selected[uid] = selected_model

        await query.answer(f"Image model set to {selected_model}")
        await query.edit_message_text(f"Image model successfully set to: {selected_model}")
        await write_state()
    else:
        await query.answer("Invalid selection.")


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.chat.id
    allowed = uid in allowlisted_uids
    if not allowed:
        await update.message.reply_text("Enter password to continue")
        await write_state()
        return

    if not context.args:
        await update.message.reply_text(
            "Please provide a prompt for the image generation, e.g., /generate_image a white siamese cat")
        await write_state()
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
            await write_state()
            return
    if not allowed:
        await update.message.reply_text("Enter password to continue")
        return

    if update.message.text and update.message.text.startswith("/generate_image"):
        return await generate_image_impl(update, update.message.text[len("/generate_image") + 1:])

    model_selected = models_selected.get(uid, "gpt-4.1")  # Updated default model
    image_model_selected = image_models_selected.get(uid, "dallee")

    if update.message.text and update.message.text.startswith("/get_model"):
        return await update.message.reply_text(model_selected)

    if update.message.text and update.message.text.startswith("/get_image_model"):
        return await update.message.reply_text(image_model_selected)

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
            image_attachments=[],
            text_attachments=[],
            base64_images=image_attachments,
        )
    )
    if update.message.chat.id < 0:
        # in group chats react on tag
        if "@noobgamgpt_bot" not in (update.message.text or update.message.caption):
            await write_state()
            return
    response = await respond_to_message_history_openai(msg_hist[uid], model_selected)
    msg_hist[uid].append(
        UserMessage(
            username=MODEL_NAME,
            msg=response,
            image_attachments=[],
            text_attachments=[],
            base64_images=[],
        )
    )
    logging.info(f"Responding with {response}")
    await update.message.reply_markdown(response)


def run_tg_bot():
    restore_state()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = Application.builder().token(os.environ["TELEGRAM_PERSONAL_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("generate_image", generate_image, has_args=1))
    app.add_handler(CommandHandler("get_model", handle_message))
    app.add_handler(CommandHandler("set_model", set_model_command))
    app.add_handler(CommandHandler("get_image_model", handle_message))
    app.add_handler(CommandHandler("set_image_model", set_image_model_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    logging.info("Polling")
    app.run_polling(poll_interval=0.5)
