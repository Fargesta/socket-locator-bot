from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import db_context.pg_context as pg_context

WAITNG_FOR_TYPE = range(1)

async def save_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = None
    try:
        user = await pg_context.get_tg_user(update.effective_user.id)
        if not user:
            raise Exception("User not found in the database.")
        
        await pg_context.create_tg_location(
            latitude=update.message.location.latitude,
            longitude=update.message.location.longitude,
            name="Test",
            socket_type="220",
            description="First location",
            layer="Test",
            created_by=user
        )
        
    except Exception as e:
        print(f"Something went wrong: {e}")
    finally:
        await pg_context.close_db()

async def ask_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    context.user_data['location'] = (location.latitude, location.longitude)
    context.user_data['messages_to_delete'] = update.message.message_id

    keyboard = [
        [InlineKeyboardButton("220V 2 Pin", callback_data="220V"), InlineKeyboardButton("380V 4 Pin", callback_data="4PIN")],
        [InlineKeyboardButton("380V 5 Pin", callback_data="5PIN"), InlineKeyboardButton("Unknown", callback_data="UNKN")],
        [InlineKeyboardButton("Cancel", callback_data="CANCEL")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    sent = await update.message.reply_text("Please select socket type:", reply_markup=reply_markup)
    context.user_data['messages_to_delete'] = [update.message.message_id, sent.message_id]

    return WAITNG_FOR_TYPE