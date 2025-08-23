import logging
from telegram import BotCommand, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from config import TG_BOT_API_KEY

# ====== HANDLERS ======
from handlers.start_handler import start, menu_handler
from handlers.chat_handler import handle_chat_text
from handlers.talk_handler import handle_talk_text
from handlers.translate_handler import handle_translate_text
from handlers.image_handler import handle_image_text

# ====== LOGGING ======
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# ====== BOT COMMANDS ======
async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "Головне меню бота")
    ])


# ====== APPLICATION ======
app = ApplicationBuilder().token(TG_BOT_API_KEY).post_init(post_init).build()

# Команди
app.add_handler(CommandHandler("start", start))

# Callback кнопки меню
app.add_handler(CallbackQueryHandler(menu_handler))


# Повідомлення тексту для різних режимів
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Делегує обробку текстових повідомлень залежно від режиму"""
    mode = context.user_data.get('mode', '')

    if mode.startswith('chat'):
        await handle_chat_text(update, context)
    elif mode.startswith('talk'):
        await handle_talk_text(update, context)
    elif mode.startswith('translate'):
        await handle_translate_text(update, context)
    elif mode.startswith('image'):
        await handle_image_text(update, context)


app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# ====== RUN ======
if __name__ == "__main__":
    app.run_polling()
