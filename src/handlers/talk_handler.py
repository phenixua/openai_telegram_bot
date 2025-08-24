import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.utils import load_messages_for_bot, get_image_path
from src.openapi_client import OpenAiClient

logger = logging.getLogger(__name__)
openai_client = OpenAiClient()

# ---------------- TALK ----------------
async def talk_with_personality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays a menu of personalities the user can talk to.

    Provides inline buttons for different personalities. Shows an image
    if available and handles both messages and callback queries.

    Args:
        update: Telegram update object containing message or callback query
        context: ContextTypes.DEFAULT_TYPE object for user session data
    """
    text = load_messages_for_bot("talk")
    image_path = get_image_path("talk")

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

    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption=text, reply_markup=reply_markup)
        else:
            await target.reply_text(text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in talk_with_personality: {e}")
        await target.reply_text(text, reply_markup=reply_markup)


async def handle_talk_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    """
    Handles callback queries when a personality is selected.

    Sets the mode to the chosen personality, sends an image if available,
    and provides a reply prompt to start the conversation.

    Args:
        update: Telegram update object containing callback query
        context: ContextTypes.DEFAULT_TYPE object for user session data
        data: Callback data indicating the selected personality
    """
    context.user_data['mode'] = data
    personality_map = {
        'talk_cobain': 'cobain',
        'talk_hawking': 'hawking',
        'talk_nietzsche': 'nietzsche',
        'talk_queen': 'queen',
        'talk_tolkien': 'tolkien'
    }
    personality = personality_map[data]
    image_path = get_image_path(f"talk_{personality}")
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message

    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption="Можете почати розмову! Напишіть повідомлення.", reply_markup=reply_markup)
        else:
            await target.reply_text("Можете почати розмову! Напишіть повідомлення.", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in talk callback: {e}")
        await target.reply_text("Можете почати розмову! Напишіть повідомлення.", reply_markup=reply_markup)
