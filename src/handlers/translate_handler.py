import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.utils import get_image_path

logger = logging.getLogger(__name__)

# ---------------- TRANSLATE MENU ----------------
async def translate_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Англійська", callback_data='translate_en')],
        [InlineKeyboardButton("Німецька", callback_data='translate_de')],
        [InlineKeyboardButton("Українська", callback_data='translate_uk')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['mode'] = ''
    target = update.message if update.message else update.callback_query.message

    # Додаємо картинку
    image_path = get_image_path("translate")
    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption="Оберіть мову для перекладу:", reply_markup=reply_markup)
        else:
            await target.reply_text("Оберіть мову для перекладу:", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in translate_menu: {e}")
        await target.reply_text("Оберіть мову для перекладу:", reply_markup=reply_markup)
