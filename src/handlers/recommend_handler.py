import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.utils import get_image_path

logger = logging.getLogger(__name__)

# ---------------- RECOMMEND ----------------
async def recommend_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the recommendation menu with options for movies, books, or music.

    Shows an image if available and presents inline buttons for each category.
    Handles the selection of a category via callback queries.

    Args:
        update: Telegram update object containing message or callback query
        context: ContextTypes.DEFAULT_TYPE object for user session data
    """
    image_path = get_image_path("recommend")  # recommend.jpg
    keyboard = [
        [InlineKeyboardButton("Фільми", callback_data='recommend_movies')],
        [InlineKeyboardButton("Книги", callback_data='recommend_books')],
        [InlineKeyboardButton("Музика", callback_data='recommend_music')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message

    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption="Оберіть категорію:", reply_markup=reply_markup)
        else:
            await target.reply_text("Оберіть категорію:", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in recommend_menu: {e}")
        await target.reply_text("Оберіть категорію:", reply_markup=reply_markup)
