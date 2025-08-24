import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, BotCommand
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
from handlers.quiz_handler import quiz_game, handle_quiz_callback, handle_quiz_answer
from handlers.recommend_handler import recommend_menu
from handlers.translate_handler import translate_menu
from handlers.talk_handler import talk_with_personality, handle_talk_callback
from utils import load_messages_for_bot, load_prompt, get_image_path
from openapi_client import OpenAiClient

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
openai_client = OpenAiClient()


# ======================= CALLBACK =======================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    target = update.message if update.message else query.message

    if data == 'start':
        context.user_data.clear()
        await start(update, context)
    elif data in ['random', 'random_again']:
        await random_fact(update, context)
    elif data == 'gpt':
        await gpt_interface(update, context)

    # TALK
    elif data == 'talk':
        await talk_with_personality(update, context)
    elif data.startswith('talk_'):
        await handle_talk_callback(update, context, data)

    # QUIZ
    elif data == 'quiz':
        await quiz_game(update, context)
    elif data.startswith('quiz_') and not data.startswith('quiz_answer'):
        await handle_quiz_callback(update, context, data)
    elif data.startswith('quiz_answer_'):
        answer = data.split('_')[-1]
        await handle_quiz_answer(update, context, answer)

    # RECOMMEND
    elif data == 'recommend':
        await recommend_menu(update, context)
    elif data.startswith('recommend_'):
        category = data.split('_')[1]
        context.user_data['recommend_category'] = category
        context.user_data['mode'] = 'recommend_genre'
        await target.reply_text(f"Введіть жанр для {category}:")

    # TRANSLATE
    elif data == 'translate':
        await translate_menu(update, context)
    elif data.startswith('translate_'):
        lang_map = {'translate_en': 'англійську', 'translate_de': 'німецьку', 'translate_uk': 'українську'}
        context.user_data['mode'] = f"translate_{data.split('_')[1]}"
        await target.reply_text(f"Надішліть текст, і я перекладу його на {lang_map[data]}.")


# ======================= TEXT =======================
async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# COMMANDS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random_fact))
app.add_handler(CommandHandler("gpt", gpt_interface))
app.add_handler(CommandHandler("talk", talk_with_personality))
app.add_handler(CommandHandler("quiz", quiz_game))
app.add_handler(CommandHandler("recommend", recommend_menu))
app.add_handler(CommandHandler("translate", translate_menu))

# MESSAGE
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

# CALLBACK
app.add_handler(CallbackQueryHandler(handle_callback))

if __name__ == "__main__":
    app.run_polling()
