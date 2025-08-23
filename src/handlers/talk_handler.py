from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.openapi_client import OpenAiClient
from src.utils import load_messages_for_bot, load_prompt

openai_client = OpenAiClient()

PERSONALITIES = {
    "cobain": "talk_cobain",
    "hawking": "talk_hawking",
    "nietzsche": "talk_nietzsche",
    "queen": "talk_queen",
    "tolkien": "talk_tolkien"
}

async def talk_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вибір особистості для спілкування"""
    context.user_data['mode'] = 'talk_select'
    text = load_messages_for_bot("talk")

    keyboard = [
        [InlineKeyboardButton("Курт Кобейн", callback_data='talk_cobain')],
        [InlineKeyboardButton("Стівен Хокінг", callback_data='talk_hawking')],
        [InlineKeyboardButton("Фрідріх Ніцше", callback_data='talk_nietzsche')],
        [InlineKeyboardButton("Фредді Мерк'юрі", callback_data='talk_queen')],
        [InlineKeyboardButton("Дж.Р.Р. Толкін", callback_data='talk_tolkien')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message
    await target.reply_text(text, reply_markup=reply_markup)

async def handle_talk_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка повідомлень у talk-режимі"""
    mode = context.user_data.get('mode', '')
    if not mode.startswith('talk_') and mode != 'talk_select':
        return

    if mode.startswith('talk_'):
        personality_key = mode.split('_')[1]
        prompt_name = f"talk_{personality_key}"
        user_text = update.message.text
        try:
            gpt_response = await openai_client.ask(user_text, load_prompt(prompt_name))
            keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(gpt_response, reply_markup=reply_markup)
        except Exception:
            await update.message.reply_text("Сталася помилка. Спробуйте пізніше.")
