from telegram import Update
from telegram.ext import ContextTypes

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка вибору меню через callback_data"""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'start':
        from handlers.start_handler import start
        await start(update, context)
    elif data == 'chat':
        from handlers.chat_handler import chat_interface
        await chat_interface(update, context)
    elif data == 'talk':
        from handlers.talk_handler import talk_interface
        await talk_interface(update, context)
    elif data == 'translate':
        from handlers.translate_handler import translate_interface
        await translate_interface(update, context)
    elif data == 'image':
        from handlers.image_handler import image_interface
        await image_interface(update, context)
