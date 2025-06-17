import os
import logging
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from flask import Flask
import database
import payments

# Initialize Flask app for health checks
flask_app = Flask(__name__)

@flask_app.route('/health')
def health():
    return "OK", 200

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram bot commands
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

def run_bot():
    """Run the Telegram bot in background"""
    application = Application.builder() \
        .token(os.getenv("TELEGRAM_TOKEN")) \
        .build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lister", register_lister))
    application.add_handler(CommandHandler("viewer", register_viewer))
    
    application.run_polling()

if __name__ == "__main__":
    # Initialize database
    database.init_db()
    
    # Start bot in background thread
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start Flask app (for health checks)
    flask_app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))

# Gunicorn will look for this
app = flask_app
