import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробляє натискання кнопок меню"""
    query = update.callback_query
    await query.answer()

    choice = query.data
    logger.info(f"User selected: {choice}")

    # Встановлюємо режим
    context.user_data['mode'] = choice

    # В залежності від вибору
    if choice == "random":
        await query.message.reply_text("🧠 Генерую випадковий факт...")
    elif choice == "gpt":
        await query.message.reply_text("🤖 Напиши своє питання для GPT:")
    elif choice == "talk":
        await query.message.reply_text("👤 Обери особистість або пиши прямо:")
    elif choice == "quiz":
        await query.message.reply_text("❓ Почнемо вікторину! Введи /quiz")
    elif choice == "recommend":
        await query.message.reply_text("🎬📚🎵 Обери: фільм, книгу чи музику")
    elif choice == "translate":
        await query.message.reply_text("🌍 Введи текст для перекладу:")
    else:
        await query.message.reply_text("⚠️ Невідомий вибір")
