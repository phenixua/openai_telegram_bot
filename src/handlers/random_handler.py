import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.openapi_client import OpenAiClient
from src.utils import load_messages_for_bot, load_prompt, get_image_path

# Ініціалізація OpenAI клієнта
openai_client = OpenAiClient()


async def random_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Інтерфейс випадкового факту.
    Викликається при виборі відповідного пункту меню.
    """
    context.user_data['mode'] = 'random'
    text = load_messages_for_bot("random")
    image_path = get_image_path("random")

    keyboard = [
        [InlineKeyboardButton("Хочу ще факт", callback_data='random_again')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message
    try:
        gpt_response = await openai_client.ask("", load_prompt("random"))
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption=f"{text}\n\n{gpt_response}", reply_markup=reply_markup)
        else:
            await target.reply_text(f"{text}\n\n{gpt_response}", reply_markup=reply_markup)
    except Exception as e:
        logging.error(f"Error in Random handler: {e}")
        await target.reply_text("⚠️ Сталася помилка. Спробуйте пізніше.")


async def handle_random_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обробка текстових повідомлень у режимі випадкових фактів.
    Зазвичай користувач тут нічого не пише, але можна додати логіку.
    """
    mode = context.user_data.get('mode', '')
    if mode != 'random':
        return  # Не в режимі random
    await random_interface(update, context)
