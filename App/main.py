import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
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

# Correct import style for Poetry
from telegram.ext import ApplicationBuilder
#from app.handlers import setup_handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_app():
    """Factory function to create the Telegram application"""
    application = ApplicationBuilder() \
        .token(os.getenv("TELEGRAM_TOKEN")) \
        .post_init(post_init) \
        .build()
    
    setup_handlers(application)
    return application

def post_init(app):
    """Runs after bot initialization"""
    print("Bot is ready!")

# Gunicorn will look for this
app = create_app()

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
    session.close()
    
    await query.edit_message_text(
        get_translation('role_registered', lang).format(role=role.capitalize())
    )

async def handle_list_property(update: Update, context: CallbackContext) -> None:
    # This will be expanded to handle property listing flow
    user_id = update.effective_user.id
    session = get_db_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if user and user.role == 'lister':
        await update.message.reply_text("Property listing flow will start here")
    else:
        await update.message.reply_text("You need to register as a lister first!")

async def handle_payment(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    amount = 10000  # ₹100 in paise
    order = create_razorpay_order(amount)
    
    if order:
        await update.message.reply_text(
            f"Please pay ₹{amount/100}:\n"
            f"Payment Link: {order['short_url']}\n\n"
            "After payment, please share the transaction ID."
        )
    else:
        await update.message.reply_text("Failed to create payment order")

def main() -> None:
    # Create the Application
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_role_selection, pattern="^role_"))
    application.add_handler(CommandHandler("list", handle_list_property))
    application.add_handler(CommandHandler("pay", handle_payment))
    
    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main()
