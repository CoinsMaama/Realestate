from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start_handler))

async def start_handler(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to Real Estate Bot!")
