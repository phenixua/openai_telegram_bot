import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.utils import load_messages_for_bot, load_prompt, get_image_path
from src.openapi_client import OpenAiClient

openai_client = OpenAiClient()
logger = logging.getLogger(__name__)


async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_messages_for_bot("random")
    prompt = load_prompt("random")
    image_path = get_image_path("random")

    keyboard = [
        [InlineKeyboardButton("Хочу ще факт", callback_data='random_again')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message

    try:
        gpt_response = await openai_client.ask("", prompt)
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(
                    photo=photo,
                    caption=f"{text}\n\n{gpt_response}",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        else:
            await target.reply_text(
                f"{text}\n\n{gpt_response}",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in random_fact: {e}")
        await target.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")
