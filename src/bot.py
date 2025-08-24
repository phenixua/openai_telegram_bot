import logging
from telegram import BotCommand, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import TG_BOT_API_KEY
from handlers.start_handler import start
from handlers.gpt_handler import gpt_interface, handle_gpt_text
from handlers.random_handler import random_fact
from handlers.talk_handler import talk_with_personality

from utils import load_messages_for_bot, get_image_path
from openapi_client import OpenAiClient

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
openai_client = OpenAiClient()


# ----------------------- QUIZ -----------------------
async def quiz_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_messages_for_bot("quiz")
    image_path = get_image_path("quiz")

    keyboard = [
        [InlineKeyboardButton("Історія", callback_data='quiz_history')],
        [InlineKeyboardButton("Наука", callback_data='quiz_science')],
        [InlineKeyboardButton("Мистецтво", callback_data='quiz_art')],
        [InlineKeyboardButton("Спорт", callback_data='quiz_sport')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message

    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        else:
            await target.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in quiz_game: {e}")
        await target.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


# ----------------------- РЕКОМЕНДАЦІЇ -----------------------
async def recommend_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Фільми", callback_data='recommend_movies')],
        [InlineKeyboardButton("Книги", callback_data='recommend_books')],
        [InlineKeyboardButton("Музика", callback_data='recommend_music')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("Оберіть категорію:", reply_markup=reply_markup)


# ----------------------- ПЕРЕКЛАДАЧ -----------------------
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
    await target.reply_text("Оберіть мову для перекладу:", reply_markup=reply_markup)


# ======================= CALLBACK =======================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    target = update.message if update.message else update.callback_query.message

    if data == 'start':
        context.user_data.clear()
        await start(update, context)

    elif data in ['random', 'random_again']:
        await random_fact(update, context)

    elif data == 'gpt':
        await gpt_interface(update, context)

    elif data == 'talk':
        await talk_with_personality(update, context)

    elif data.startswith('talk_'):
        context.user_data['mode'] = data
        await talk_with_personality(update, context)

    elif data == 'quiz':
        await quiz_game(update, context)

    elif data.startswith('quiz_'):
        context.user_data['mode'] = data
        await quiz_game(update, context)

    elif data == 'recommend':
        await recommend_menu(update, context)

    elif data.startswith('recommend_'):
        category = data.split('_')[1]
        context.user_data['recommend_category'] = category
        context.user_data['mode'] = 'recommend_genre'
        await target.reply_text(f"Введіть жанр для {category}:")

    elif data == 'translate':
        await translate_menu(update, context)

    elif data.startswith('translate_'):
        lang_map = {'translate_en': 'англійську', 'translate_de': 'німецьку', 'translate_uk': 'українську'}
        context.user_data['mode'] = f"translate_{data.split('_')[1]}"
        await target.reply_text(f"Надішліть текст, і я перекладу його на {lang_map[data]}.")


# ======================= TEXT =======================
async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode = context.user_data.get('mode', '')
    if user_mode == 'gpt':
        await handle_gpt_text(update, context)
    else:
        await update.message.reply_text("Режим ще не реалізований для текстових повідомлень.")


# ======================= RUN =======================
async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "Головне меню бота"),
        BotCommand("random", "Випадковий факт · 🧠"),
        BotCommand("gpt", "GPT-чат · 🤖"),
        BotCommand("talk", "Розмова з особистістю · 👤"),
        BotCommand("quiz", "Квіз · ❓"),
        BotCommand("recommend", "Рекомендації фільми/книги/музика 🎬📚🎵"),
        BotCommand("translate", "Перекладач 🌍")
    ])


app = ApplicationBuilder().token(TG_BOT_API_KEY).post_init(post_init).build()

# Команди
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random_fact))
app.add_handler(CommandHandler("gpt", gpt_interface))
app.add_handler(CommandHandler("talk", talk_with_personality))
app.add_handler(CommandHandler("quiz", quiz_game))
app.add_handler(CommandHandler("recommend", recommend_menu))
app.add_handler(CommandHandler("translate", translate_menu))

# Повідомлення
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

# Callback кнопки
app.add_handler(CallbackQueryHandler(handle_callback))

if __name__ == "__main__":
    app.run_polling()
