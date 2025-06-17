import os
import logging
import threading
from flask import Flask, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CallbackContext
)
from app.database import get_db_session, User
from app.payments import create_razorpay_order
from app.translations import get_translation
from app.handlers import setup_handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create Flask app for Gunicorn (web server component)
flask_app = Flask(__name__)

# Global variable for telegram application
telegram_application = None

@flask_app.route('/')
def health_check():
    """Health check endpoint for Render.com"""
    return jsonify({
        "status": "running",
        "message": "Telegram bot is active",
        "bot_running": telegram_application is not None
    })

@flask_app.route('/status')
def bot_status():
    """Bot status endpoint"""
    if telegram_application:
        return jsonify({"bot": "running", "status": "healthy"})
    else:
        return jsonify({"bot": "not_running", "status": "error"}), 500

def create_telegram_app():
    """Factory function to create the Telegram application"""
    application = ApplicationBuilder() \
        .token(os.getenv("TELEGRAM_TOKEN")) \
        .post_init(post_init) \
        .build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_role_selection, pattern="^role_"))
    application.add_handler(CommandHandler("list", handle_list_property))
    application.add_handler(CommandHandler("pay", handle_payment))
    
    # Setup additional handlers from your handlers module
    setup_handlers(application)
    
    return application

def post_init(app):
    """Runs after bot initialization"""
    logger.info("Bot is ready!")
    print("Bot is ready!")

# Command handlers
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    lang = 'en'  # Default language
    
    keyboard = [
        [InlineKeyboardButton("🏠 Lister", callback_data="role_lister")],
        [InlineKeyboardButton("👀 Viewer", callback_data="role_viewer")]
    ]
    
    await update.message.reply_text(
        get_translation('welcome', lang).format(name=user.first_name),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_role_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    role = query.data.split('_')[1]
    user_id = query.from_user.id
    lang = 'en'  # Default language
    
    # Save user to database
    session = get_db_session()
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            user = User(
                telegram_id=user_id,
                name=query.from_user.full_name,
                role=role
            )
            session.add(user)
        else:
            user.role = role
            
        session.commit()
        
        await query.edit_message_text(
            get_translation('role_registered', lang).format(role=role.capitalize())
        )
    except Exception as e:
        logger.error(f"Database error: {e}")
        await query.edit_message_text("Sorry, there was an error. Please try again.")
    finally:
        session.close()

async def handle_list_property(update: Update, context: CallbackContext) -> None:
    # This will be expanded to handle property listing flow
    user_id = update.effective_user.id
    session = get_db_session()
    
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        
        if user and user.role == 'lister':
            await update.message.reply_text("Property listing flow will start here")
        else:
            await update.message.reply_text("You need to register as a lister first! Use /start to register.")
    except Exception as e:
        logger.error(f"Database error: {e}")
        await update.message.reply_text("Sorry, there was an error. Please try again.")
    finally:
        session.close()

async def handle_payment(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    amount = 10000  # ₹100 in paise
    
    try:
        order = create_razorpay_order(amount)
        
        if order:
            await update.message.reply_text(
                f"Please pay ₹{amount/100}:\n"
                f"Payment Link: {order['short_url']}\n\n"
                "After payment, please share the transaction ID."
            )
        else:
            await update.message.reply_text("Failed to create payment order")
    except Exception as e:
        logger.error(f"Payment error: {e}")
        await update.message.reply_text("Sorry, payment service is temporarily unavailable.")

def run_telegram_bot():
    """Function to run the telegram bot in a separate thread"""
    global telegram_application
    
    try:
        telegram_application = create_telegram_app()
        logger.info("Starting Telegram bot...")
        telegram_application.run_polling(
            drop_pending_updates=True,
            close_loop=False
        )
    except Exception as e:
        logger.error(f"Error running Telegram bot: {e}")

def start_bot_in_background():
    """Start the Telegram bot in a background thread"""
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    logger.info("Telegram bot thread started")

# Start the bot when the module is imported (but not when run directly)
if __name__ != "__main__":
    # This runs when Gunicorn imports the module
    start_bot_in_background()

# This is what Gunicorn will use as the WSGI application
app = flask_app

def main() -> None:
    """Main function for direct execution (development mode)"""
    logger.info("Running in development mode...")
    
    # Start Flask server in a separate thread for development
    flask_thread = threading.Thread(
        target=lambda: flask_app.run(host='0.0.0.0', port=5000, debug=False),
        daemon=True
    )
    flask_thread.start()
    
    # Run telegram bot in main thread
    run_telegram_bot()

if __name__ == "__main__":
    main()
