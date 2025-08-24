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

# ======================= LOGGING =======================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======================= OPENAI CLIENT =======================
openai_client = OpenAiClient()


# ======================= BOT INITIALIZATION =======================
async def post_init(application):
    """
    Set up Telegram bot commands visible in the app's menu.

    Args:
        application: Telegram Application instance.
    """
    await application.bot.set_my_commands([
        BotCommand("start", "Main menu of the bot"),
        BotCommand("random", "Random fact · 🧠"),
        BotCommand("gpt", "GPT chat · 🤖"),
        BotCommand("talk", "Talk with a personality · 👤"),
        BotCommand("quiz", "Quiz · ❓"),
        BotCommand("recommend", "Recommendations: movies/books/music 🎬📚🎵"),
        BotCommand("translate", "Translator 🌍")
    ])


def main():
    """
    Main function to start the Telegram bot.

    Initializes the Application, registers handlers for commands, messages, and callbacks,
    and starts polling for updates.
    """
    # Initialize the bot application
    app = ApplicationBuilder().token(TG_BOT_API_KEY).post_init(post_init).build()

    # ---------------- COMMAND HANDLERS ----------------
    # Add handlers for bot commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random_fact))
    app.add_handler(CommandHandler("gpt", gpt_interface))
    app.add_handler(CommandHandler("talk", talk_with_personality))
    app.add_handler(CommandHandler("quiz", quiz_game))
    app.add_handler(CommandHandler("recommend", recommend_menu))
    app.add_handler(CommandHandler("translate", translate_menu))

    # ---------------- MESSAGE HANDLER ----------------
    # Handle user text messages that are not commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    # ---------------- CALLBACK HANDLER ----------------
    # Handle button clicks from inline keyboards
    app.add_handler(CallbackQueryHandler(handle_callback))

    # ---------------- RUN BOT ----------------
    logger.info("Bot is running. Waiting for messages...")
    app.run_polling()


if __name__ == "__main__":
    main()
