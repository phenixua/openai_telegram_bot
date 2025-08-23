from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.openapi_client import OpenAiClient
from src.utils import load_prompt

openai_client = OpenAiClient()

async def chat_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вхід у режим GPT-чат"""
    context.user_data['mode'] = 'chat'
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("💬 Ви в GPT-чаті. Напишіть ваше питання:", reply_markup=reply_markup)

async def handle_chat_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка повідомлень у chat-режимі"""
    if context.user_data.get('mode') != 'chat':
        return
    user_text = update.message.text
    try:
        gpt_response = await openai_client.ask(user_text, load_prompt("gpt"))
        await update.message.reply_text(gpt_response)
    except Exception:
        await update.message.reply_text("Сталася помилка. Спробуйте пізніше.")
