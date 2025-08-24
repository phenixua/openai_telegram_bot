import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.utils import get_image_path

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the main menu of the bot.

    Provides quick access to all primary bot commands via inline buttons.
    Shows an image if available and handles both messages and callback queries.

    Args:
        update: Telegram update object containing message or callback query
        context: ContextTypes.DEFAULT_TYPE object for user session data
    """
    text_main = (
        "Привіт! Цей бот поєднує в собі зручність Telegram та потужність ChatGPT\n\n"
        "Корисні команди та посилання:\n"
        "1. /start — головне меню бота\n"
        "2. /random - дізнатись випадковий факт · 🧠\n"
        "3. /gpt - Задати питання ChatGPT · 🤖\n"
        "4. /talk - поговорити з відомою особистістю · 👤\n"
        "5. /quiz - перевірити свої знання ❓\n"
        "6. /recommend - Рекомендації фільми/книги/музика 🎬📚🎵\n"
        "7. /translate - переклад тексту 🌍"
    )

    image_path = get_image_path("main")

    keyboard = [
        [InlineKeyboardButton("Випадковий факт", callback_data='random')],
        [InlineKeyboardButton("GPT-чат", callback_data='gpt')],
        [InlineKeyboardButton("Розмова з особистістю", callback_data='talk')],
        [InlineKeyboardButton("Квіз", callback_data='quiz')],
        [InlineKeyboardButton("Рекомендації фільми/книги/музика", callback_data='recommend')],
        [InlineKeyboardButton("Перекладач", callback_data='translate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message
    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(
                    photo=photo,
                    caption=text_main,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        else:
            await target.reply_text(
                text_main,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logging.error(f"Error in start: {e}")
        await target.reply_text(text_main, reply_markup=reply_markup, parse_mode='Markdown')
