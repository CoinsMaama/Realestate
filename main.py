import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext
)
import database
import payments

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🏠 Welcome to Real Estate Bot!\n"
        "Choose your role:\n"
        "/lister - Post properties\n"
        "/viewer - Browse properties"
    )

async def register_lister(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    database.save_user(user_id, "lister")
    payment_link = payments.create_razorpay_link(10000)  # ₹100
    await update.message.reply_text(
        f"✅ Registered as Lister!\n"
        f"Pay ₹100 to post your first property:\n{payment_link}"
    )

async def register_viewer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    database.save_user(user_id, "viewer")
    await update.message.reply_text(
        "✅ Registered as Viewer!\n"
        "Use /browse to see available properties"
    )

def main():
    # Create bot application
    application = Application.builder() \
        .token(os.getenv("TELEGRAM_TOKEN")) \
        .build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lister", register_lister))
    application.add_handler(CommandHandler("viewer", register_viewer))
    
    # Start polling
    application.run_polling()

if __name__ == "__main__":
    database.init_db()  # Initialize database
    main()
