from config import TG_BOT_API_KEY
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from utils import load_messages_for_bot, load_prompt, get_image_path
from openapi_client import OpenAiClient
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

openai_client = OpenAiClient()


# ======================= ФУНКЦІЇ =======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_main = (
        "Привіт! Цей бот поєднує в собі зручність Telegram та потужність ChatGPT\n\n"
        "Корисні команди та посилання:\n"
        "1. /start — головне меню бота\n"
        "2. /random - дізнатись випадковий факт · 🧠\n"
        "3. /gpt - Задати питання ChatGPT · 🤖\n"
        "4. /talk - поговорити з відомою особистістю · 👤\n"
        "5. /quiz - перевірити свої знання ❓\n"
        "6. /recommend - Рекомендації фільми/книги/музика 🎬📚🎵\n"
        "7. /translate - переклад тексту 🌍"
    )
    image_path = get_image_path("main")

    keyboard = [
        [InlineKeyboardButton("Випадковий факт", callback_data='random')],
        [InlineKeyboardButton("GPT-чат", callback_data='gpt')],
        [InlineKeyboardButton("Розмова з особистістю", callback_data='talk')],
        [InlineKeyboardButton("Квіз", callback_data='quiz')],
        [InlineKeyboardButton("Рекомендації фільми/книги/музика", callback_data='recommend')],
        [InlineKeyboardButton("Перекладач", callback_data='translate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message
    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption=text_main, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await target.reply_text(text_main, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in start: {e}")
        await target.reply_text(text_main, reply_markup=reply_markup, parse_mode='Markdown')


# ----------------------- РАНДОМ -----------------------
async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_messages_for_bot("random")
    prompt = load_prompt("random")
    image_path = get_image_path("random")

    keyboard = [
        [InlineKeyboardButton("Хочу ще факт", callback_data='random_again')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        gpt_response = await openai_client.ask("", prompt)
        target = update.message if update.message else update.callback_query.message
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption=f"{text}\n\n{gpt_response}", reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await target.reply_text(f"{text}\n\n{gpt_response}", reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in random_fact: {e}")
        target = update.message if update.message else update.callback_query.message
        await target.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")


# ----------------------- GPT -----------------------
async def gpt_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_messages_for_bot("gpt")
    image_path = get_image_path("gpt")
    context.user_data['mode'] = 'gpt'

    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message
    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption=text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in gpt_interface: {e}")
        await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


# ----------------------- TALK -----------------------
async def talk_with_personality(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                await target.reply_photo(photo=photo, caption=text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in talk_with_personality: {e}")
        await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


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
                await target.reply_photo(photo=photo, caption=text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in quiz_game: {e}")
        await target.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


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
        personality_map = {
            'talk_cobain': 'cobain',
            'talk_hawking': 'hawking',
            'talk_nietzsche': 'nietzsche',
            'talk_queen': 'queen',
            'talk_tolkien': 'tolkien'
        }
        context.user_data['mode'] = data
        personality = personality_map[data]
        image_path = get_image_path(f"talk_{personality}")
        keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            if image_path:
                with open(image_path, 'rb') as photo:
                    await query.message.reply_photo(photo=photo, caption="Можете почати розмову! Напишіть повідомлення.", reply_markup=reply_markup)
            else:
                await query.message.reply_text("Можете почати розмову! Напишіть повідомлення.", reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Error in talk callback: {e}")
            await query.message.reply_text("Можете почати розмову! Напишіть повідомлення.", reply_markup=reply_markup)

    elif data == 'quiz':
        await quiz_game(update, context)

    elif data.startswith('quiz_'):
        if data == 'quiz_change_topic':
            await quiz_game(update, context)
            return
        context.user_data['mode'] = data
        topic = data.split('_')[1]
        if 'score' not in context.user_data:
            context.user_data['score'] = 0
        topic_prompts = {
            'history': 'Створи одне цікаве питання з історії з 4 варіантами відповідей. Формат: Питання? A) ... B) ... C) ... D) ...',
            'science': 'Створи одне цікаве питання з науки з 4 варіантами відповідей. Формат: Питання? A) ... B) ... C) ... D) ...',
            'art': 'Створи одне цікаве питання з мистецтва з 4 варіантами відповідей. Формат: Питання? A) ... B) ... C) ... D) ...',
            'sport': 'Створи одне цікаве питання зі спорту з 4 варіантами відповідей. Формат: Питання? A) ... B) ... C) ... D) ...'
        }
        try:
            gpt_response = await openai_client.ask(topic_prompts[topic], load_prompt("quiz"))
            context.user_data['quiz_question'] = gpt_response
            await query.message.reply_text(f"{gpt_response}\n\nНапишіть вашу відповідь (A, B, C або D):")
        except Exception as e:
            logging.error(f"Error in quiz: {e}")
            await query.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")

    elif data == 'recommend':
        await recommend_menu(update, context)

    elif data.startswith('recommend_'):
        category = data.split('_')[1]
        context.user_data['recommend_category'] = category
        context.user_data['mode'] = 'recommend_genre'
        target = update.message if update.message else update.callback_query.message
        await target.reply_text(f"Введіть жанр для {category}:")

    elif data == 'translate':
        await translate_menu(update, context)

    elif data.startswith('translate_'):
        lang_map = {
            'translate_en': 'англійську',
            'translate_de': 'німецьку',
            'translate_uk': 'українську'
        }
        context.user_data['mode'] = f"translate_{data.split('_')[1]}"
        await query.message.reply_text(f"Надішліть текст, і я перекладу його на {lang_map[data]}.")


# ======================= TEXT =======================
async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode = context.user_data.get('mode', '')
    user_text = update.message.text

    if user_mode == 'gpt':
        prompt = load_prompt("gpt")
        try:
            gpt_response = await openai_client.ask(user_text, prompt)
            await update.message.reply_text(gpt_response)
        except Exception as e:
            logging.error(f"Error in gpt mode: {e}")
            await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")

    elif user_mode.startswith('talk'):
        personality = user_mode.split('_')[1]
        prompt = load_prompt(f"talk_{personality}")
        keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            gpt_response = await openai_client.ask(user_text, prompt)
            await update.message.reply_text(gpt_response, reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Error in talk mode: {e}")
            await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")

    elif user_mode.startswith('quiz'):
        topic = user_mode.split('_')[1]
        score = context.user_data.get('score', 0)
        if 'quiz_question' in context.user_data:
            try:
                check_prompt = f"Користувач відповів: '{user_text}' на питання: '{context.user_data['quiz_question']}'. Скажи чи правильна відповідь (так/ні) та дай коротке пояснення."
                gpt_response = await openai_client.ask(check_prompt, "Ти експерт з квізів. Перевіряй відповіді користувачів.")
                is_correct = "так" in gpt_response.lower() or "правильн" in gpt_response.lower()
                if is_correct:
                    context.user_data['score'] = score + 1
                current_score = context.user_data.get('score', 0)
                keyboard = [
                    [InlineKeyboardButton("Ще питання", callback_data=f'quiz_{topic}')],
                    [InlineKeyboardButton("Змінити тему", callback_data='quiz_change_topic')],
                    [InlineKeyboardButton("Головне меню", callback_data='start')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(f"{gpt_response}\n\nВаш рахунок: {current_score}", reply_markup=reply_markup)
                del context.user_data['quiz_question']
            except Exception as e:
                logging.error(f"Error in quiz mode: {e}")
                await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")

    elif user_mode == 'recommend_genre':
        category = context.user_data.get('recommend_category', '')
        prompt = f"Порадуй користувача {category} за жанром {user_text}, дай 3 рекомендації у вигляді списку."
        try:
            gpt_response = await openai_client.ask(prompt, "")
            keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(gpt_response, reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Error in recommend mode: {e}")
            await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")

    elif user_mode.startswith('translate'):
        lang_code = user_mode.split('_')[1]
        lang_map = {
            'en': 'англійську',
            'de': 'німецьку',
            'uk': 'українську'
        }
        prompt = f"Переклади наступний текст на {lang_map[lang_code]}:\n\n{user_text}"
        try:
            gpt_response = await openai_client.ask(prompt, "")
            keyboard = [[InlineKeyboardButton("Головне меню", callback_data='start')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(gpt_response, reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Error in translate mode: {e}")
            await update.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")


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

app.run_polling()
