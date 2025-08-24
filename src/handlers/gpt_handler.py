import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.utils import load_messages_for_bot, load_prompt, get_image_path
from src.openapi_client import OpenAiClient

openai_client = OpenAiClient()
logger = logging.getLogger(__name__)

async def gpt_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends the GPT interface message with an optional image and sets the user's mode.

    Args:
        update (Update): Incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): Context object for user data and bot interaction.
    """
    text = load_messages_for_bot("gpt")
    image_path = get_image_path("gpt")
    context.user_data['mode'] = 'gpt'

    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message
    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        else:
            await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in gpt_interface: {e}")
        await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_gpt_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles user text messages in GPT mode and sends the AI-generated response.

    Args:
        update (Update): Incoming update containing the user's message.
        context (ContextTypes.DEFAULT_TYPE): Context object for user data and bot interaction.
    """
    user_text = update.message.text
    prompt = load_prompt("gpt")
    try:
        gpt_response = await openai_client.ask(user_text, prompt)
        await update.message.reply_text(gpt_response)
    except Exception as e:
        logger.error(f"Error in gpt text handling: {e}")
        await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")
