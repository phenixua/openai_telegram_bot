from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.start_handler import start
from src.handlers.gpt_handler import gpt_interface
from src.handlers.random_handler import random_fact
from src.handlers.quiz_handler import quiz_game, handle_quiz_callback, handle_quiz_answer
from src.handlers.recommend_handler import recommend_menu
from src.handlers.translate_handler import translate_menu
from src.handlers.talk_handler import talk_with_personality, handle_talk_callback


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all callback queries from inline buttons in the bot.

    Depending on the callback data, this function routes the user
    to the appropriate handler (start, random fact, GPT chat, talk,
    quiz, recommendations, or translation).

    Args:
        update: Telegram update object containing callback query
        context: ContextTypes.DEFAULT_TYPE object for user session data
    """
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
        lang_map = {
            'translate_en': 'англійську',
            'translate_de': 'німецьку',
            'translate_uk': 'українську'
        }
        context.user_data['mode'] = f"translate_{data.split('_')[1]}"
        await target.reply_text(
            f"Надішліть текст, і я перекладу його на {lang_map[data]}."
        )
