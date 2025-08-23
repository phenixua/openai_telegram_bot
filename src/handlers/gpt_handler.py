# src/handlers/gpt_handler.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.openapi_client import OpenAiClient
from src.utils import load_messages_for_bot, load_prompt

# Ініціалізація клієнта
openai_client = OpenAiClient()


async def chat_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Інтерфейс режиму спілкування з GPT.
    Викликається при виборі '💬 Спілкування з GPT'.
    """
    context.user_data['mode'] = 'gpt'
    text = load_messages_for_bot("gpt")
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message
    await target.reply_text(text, reply_markup=reply_markup)


async def handle_gpt_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обробка повідомлень користувача у режимі GPT.
    """
    user_mode = context.user_data.get('mode', '')
    if user_mode != 'gpt':
        return

    user_text = update.message.text
    prompt = load_prompt("gpt")

    try:
        gpt_response = await openai_client.ask(user_text, prompt)
        await update.message.reply_text(gpt_response)
    except Exception as e:
        logging.error(f"Error in GPT handler: {e}")
        await update.message.reply_text("⚠️ Виникла помилка при зверненні до GPT.")
