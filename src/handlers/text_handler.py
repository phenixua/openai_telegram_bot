import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.utils import load_prompt
from src.openapi_client import OpenAiClient
from src.handlers.gpt_handler import handle_gpt_text

logger = logging.getLogger(__name__)
openai_client = OpenAiClient()


async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles incoming text messages based on the user's current mode.

    Depending on the user's mode stored in context.user_data['mode'], this function
    routes the message to GPT chat, conversation with a personality, recommendations by genre,
    translation mode, or shows a prompt to choose a bot mode.

    Args:
        update: Telegram update object containing the incoming message
        context: ContextTypes.DEFAULT_TYPE object for user session data
    """
    user_mode = context.user_data.get('mode', '')
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if user_mode == 'gpt':
        await handle_gpt_text(update, context)

    elif user_mode.startswith('talk'):
        personality = user_mode.split('_')[1]
        prompt = load_prompt(f"talk_{personality}")
        try:
            gpt_response = await openai_client.ask(update.message.text, prompt)
            await update.message.reply_text(gpt_response, reply_markup=reply_markup)
        except Exception as e:
            logger.error(f"Error in talk mode: {e}")
            await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.", reply_markup=reply_markup)

    elif user_mode == 'recommend_genre':
        category = context.user_data.get('recommend_category', '')
        prompt = f"Порадуй користувача {category} за жанром {update.message.text}, дай 3 рекомендації у вигляді списку."
        try:
            gpt_response = await openai_client.ask(prompt, "")
            await update.message.reply_text(gpt_response, reply_markup=reply_markup)
        except Exception as e:
            logger.error(f"Error in recommend mode: {e}")
            await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.", reply_markup=reply_markup)

    elif user_mode.startswith('translate'):
        lang_code = user_mode.split('_')[1]
        lang_map = {'en': 'англійську', 'de': 'німецьку', 'uk': 'українську'}
        prompt = f"Переклади наступний текст на {lang_map[lang_code]}:\n\n{update.message.text}"
        try:
            gpt_response = await openai_client.ask(prompt, "")
            await update.message.reply_text(gpt_response, reply_markup=reply_markup)
        except Exception as e:
            logger.error(f"Error in translate mode: {e}")
            await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.", reply_markup=reply_markup)

    else:
        await update.message.reply_text("Оберіть режим бота через меню.", reply_markup=reply_markup)
