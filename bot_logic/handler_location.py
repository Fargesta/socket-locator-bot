from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
import db_context.pg_context as pg_context
from bot_logic.handler_cancel import cancel

SOCKET_TYPE, SOCKET_DESCRIPTION = range(1, 5)

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

async def handle_location_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    location = update.message.location
    context.user_data["location"] = (location.latitude, location.longitude)
    context.user_data["messages_to_delete"] = [update.message.message_id]

    keyboard = [
        [InlineKeyboardButton("220V 2 pin", callback_data="220V"), InlineKeyboardButton("380V 4 pin", callback_data="4PIN")],
        [InlineKeyboardButton("380V 5 pin", callback_data="5PIN"), InlineKeyboardButton("Don't know", callback_data="UNKN")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")],
    ]
    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('<b>Please choose socket type:</b>', parse_mode='HTML', reply_markup=reply_markup)
    return SOCKET_TYPE

async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selection = update.message.text

    if selection == "/cancel":
        return await cancel(update, context)

    location = context.user_data.get("location")

    await update.message.reply_text(
        f"You selected '{selection}' with location: {location}",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
