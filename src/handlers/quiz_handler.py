import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.utils import load_messages_for_bot, load_prompt, get_image_path
from src.openapi_client import OpenAiClient

openai_client = OpenAiClient()
logger = logging.getLogger(__name__)

# ---------------- QUIZ GAME ----------------
async def quiz_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the quiz menu with available topics and optional image support.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): The context with user data.
    """
    text = load_messages_for_bot("quiz")
    keyboard = [
        [InlineKeyboardButton("Історія", callback_data='quiz_history')],
        [InlineKeyboardButton("Наука", callback_data='quiz_science')],
        [InlineKeyboardButton("Мистецтво", callback_data='quiz_art')],
        [InlineKeyboardButton("Спорт", callback_data='quiz_sport')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    target = update.message if update.message else update.callback_query.message

    image_path = get_image_path("quiz")
    try:
        if image_path:
            with open(image_path, 'rb') as photo:
                await target.reply_photo(photo=photo, caption=text, reply_markup=reply_markup)
        else:
            await target.reply_text(text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in quiz_game: {e}")
        await target.reply_text(text, reply_markup=reply_markup)

# ---------------- HANDLE QUIZ CALLBACK ----------------
async def handle_quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    """
    Handles user's topic selection in the quiz menu and generates a quiz question.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): The context with user data.
        data (str): Callback data from the selected topic button.
    """
    if data == 'quiz_change_topic':
        await quiz_game(update, context)
        return

    topic = data.split('_')[1]
    context.user_data['mode'] = f'quiz_{topic}'
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

        keyboard = [
            [
                InlineKeyboardButton("A", callback_data='quiz_answer_A'),
                InlineKeyboardButton("B", callback_data='quiz_answer_B'),
                InlineKeyboardButton("C", callback_data='quiz_answer_C'),
                InlineKeyboardButton("D", callback_data='quiz_answer_D')
            ],
            [InlineKeyboardButton("Головне меню", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(
            f"{gpt_response}\n\nОберіть вашу відповідь:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in quiz callback: {e}")
        await update.callback_query.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")

# ---------------- HANDLE QUIZ ANSWER ----------------
async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, answer: str):
    """
    Evaluates the user's answer to a quiz question using GPT and updates the score.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): The context with user data.
        answer (str): User's answer (A, B, C, D).
    """
    topic = context.user_data.get('mode', '').split('_')[1]
    score = context.user_data.get('score', 0)

    if 'quiz_question' not in context.user_data:
        await update.callback_query.message.reply_text("Оберіть тему та почніть квіз заново.")
        return

    try:
        check_prompt = (
            f"Користувач відповів: '{answer}' на питання: '{context.user_data['quiz_question']}'. "
            "Скажи чи правильна відповідь (так/ні) та дай коротке пояснення."
        )
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

        await update.callback_query.message.reply_text(
            f"{gpt_response}\n\nВаш рахунок: {current_score}",
            reply_markup=reply_markup
        )

        del context.user_data['quiz_question']

    except Exception as e:
        logger.error(f"Error in quiz answer: {e}")
        await update.callback_query.message.reply_text("Вибачте, сталася помилка. Спробуйте пізніше.")
