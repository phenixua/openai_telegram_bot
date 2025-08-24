import logging
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from config import TG_BOT_API_KEY
from handlers.start_handler import start
from handlers.gpt_handler import gpt_interface
from handlers.random_handler import random_fact
from handlers.quiz_handler import quiz_game
from handlers.recommend_handler import recommend_menu
from handlers.translate_handler import translate_menu
from handlers.talk_handler import talk_with_personality
from handlers.text_handler import handle_text_messages
from handlers.callback_handler import handle_callback
from openapi_client import OpenAiClient


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
openai_client = OpenAiClient()


# ======================= RUN =======================
async def post_init(application):
    """
    Initialize bot commands when the Telegram bot starts.

    Args:
        application: Telegram application instance
    """
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

# COMMAND HANDLERS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random_fact))
app.add_handler(CommandHandler("gpt", gpt_interface))
app.add_handler(CommandHandler("talk", talk_with_personality))
app.add_handler(CommandHandler("quiz", quiz_game))
app.add_handler(CommandHandler("recommend", recommend_menu))
app.add_handler(CommandHandler("translate", translate_menu))

# MESSAGE HANDLER
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

# CALLBACK HANDLER
app.add_handler(CallbackQueryHandler(handle_callback))


if __name__ == "__main__":
    app.run_polling()
