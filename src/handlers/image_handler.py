from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.openapi_client import OpenAiClient

openai_client = OpenAiClient()

async def image_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'image'
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("🖼 Надішліть опис для генерації зображення:", reply_markup=reply_markup)

async def handle_image_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('mode') != 'image':
        return
    user_text = update.message.text
    try:
        gpt_response = await openai_client.ask(f"Створи опис для зображення: {user_text}", "")
        await update.message.reply_text(f"Ось ваш опис: {gpt_response}")
    except Exception:
        await update.message.reply_text("Сталася помилка. Спробуйте пізніше.")
