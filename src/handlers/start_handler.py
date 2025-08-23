# src/handlers/start_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.handlers.menu_handler import menu_handler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Головне меню"""
    context.user_data['mode'] = 'menu'

    keyboard = [
        [InlineKeyboardButton("💬 Спілкування з GPT", callback_data='chat')],
        [InlineKeyboardButton("🗣 Спілкування з відомою особистістю", callback_data='talk')],
        [InlineKeyboardButton("🌍 Перекладач", callback_data='translate')],
        [InlineKeyboardButton("🖼 Зображення", callback_data='image')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message
    await target.reply_text("👋 Вітаю! Оберіть режим роботи:", reply_markup=reply_markup)
