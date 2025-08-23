import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.openapi_client import OpenAiClient
from src.utils import load_messages_for_bot, load_prompt

# Ініціалізація OpenAI клієнта
openai_client = OpenAiClient()

QUIZ_TOPICS = {
    "history": "Створи одне цікаве питання з історії з 4 варіантами відповідей. Формат: Питання? A) ... B) ... C) ... D) ...",
    "science": "Створи одне цікаве питання з науки з 4 варіантами відповідей. Формат: Питання? A) ... B) ... C) ... D) ...",
    "art": "Створи одне цікаве питання з мистецтва з 4 варіантами відповідей. Формат: Питання? A) ... B) ... C) ... D) ...",
    "sport": "Створи одне цікаве питання зі спорту з 4 варіантами відповідей. Формат: Питання? A) ... B) ... C) ... D) ..."
}


async def quiz_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вибір теми для квізу"""
    context.user_data['mode'] = 'quiz_select'
    text = load_messages_for_bot("quiz")
    image_path = None  # Можна додати get_image_path("quiz") якщо є

    keyboard = [
        [InlineKeyboardButton("Історія", callback_data='quiz_history')],
        [InlineKeyboardButton("Наука", callback_data='quiz_science')],
        [InlineKeyboardButton("Мистецтво", callback_data='quiz_art')],
        [InlineKeyboardButton("Спорт", callback_data='quiz_sport')],
        [InlineKeyboardButton("Головне меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = update.message if update.message else update.callback_query.message
    await target.reply_text(text, reply_markup=reply_markup)


async def generate_quiz_question(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
    """Генерація одного питання по темі"""
    context.user_data['mode'] = f"quiz_{topic}"
    if 'score' not in context.user_data:
        context.user_data['score'] = 0

    try:
        prompt_text = QUIZ_TOPICS[topic]
        gpt_response = await openai_client.ask(prompt_text, load_prompt("quiz"))
        context.user_data['quiz_question'] = gpt_response

        await update.callback_query.message.reply_text(
            f"{gpt_response}\n\nНапишіть вашу відповідь (A, B, C або D):"
        )
    except Exception as e:
        logging.error(f"Error generating quiz question: {e}")
        await update.callback_query.message.reply_text("⚠️ Сталася помилка. Спробуйте пізніше.")


async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка відповіді користувача на питання квізу"""
    user_mode = context.user_data.get('mode', '')
    if not user_mode.startswith('quiz_') or 'quiz_question' not in context.user_data:
        return  # Не в режимі quiz або питання не задано

    topic = user_mode.split('_')[1]
    user_text = update.message.text
    score = context.user_data.get('score', 0)

    try:
        check_prompt = (
            f"Користувач відповів: '{user_text}' на питання: '{context.user_data['quiz_question']}'. "
            "Скажи, чи правильна відповідь (так/ні) та дай коротке пояснення."
        )
        gpt_response = await openai_client.ask(check_prompt, "Ти експерт з квізів. Перевіряй відповіді користувачів.")

        is_correct = "так" in gpt_response.lower() or "правильн" in gpt_response.lower()
        if is_correct:
            context.user_data['score'] = score + 1

        current_score = context.user_data.get('score', 0)
        keyboard = [
            [InlineKeyboardButton("Ще питання", callback_data=f'quiz_{topic}')],
            [InlineKeyboardButton("Змінити тему", callback_data='quiz_select')],
            [InlineKeyboardButton("Головне меню", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f"{gpt_response}\n\nВаш рахунок: {current_score}", reply_markup=reply_markup)
        del context.user_data['quiz_question']

    except Exception as e:
        logging.error(f"Error handling quiz answer: {e}")
        await update.message.reply_text("⚠️ Сталася помилка. Спробуйте пізніше.")
