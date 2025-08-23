from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.openapi_client import OpenAiClient

openai_client = OpenAiClient()

async def translate_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'translate'
    keyboard = [
        [InlineKeyboardButton("Англійська", callback_data='translate_en')],
        [InlineKeyboardButton("Німецька", callback_data='translate_de')],
        [InlineKeyboardButton("Іспанська", callback_data='translate_es')],
        [InlineKeyboardButton("Українська", callback_data='translate_uk')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("Оберіть мову перекладу:", reply_markup=reply_markup)

async def handle_translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('mode', '').startswith('translate'):
        return
    user_text = update.message.text
    lang = context.user_data.get('mode').split('_')[1]
    lang_map = {'en':'англійську','de':'німецьку','es':'іспанську','uk':'українську'}
    prompt = f"Переклади на {lang_map[lang]}:\n{user_text}"
    try:
        gpt_response = await openai_client.ask(prompt, "")
        await update.message.reply_text(gpt_response)
    except Exception:
        await update.message.reply_text("Сталася помилка. Спробуйте пізніше.")
