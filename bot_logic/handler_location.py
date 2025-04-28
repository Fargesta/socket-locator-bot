from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import bot_logic.return_states as rs        

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    context.user_data["location"] = (location.latitude, location.longitude)
    context.user_data["messages_to_delete"] = [update.message.message_id]

    keyboard = [
        [InlineKeyboardButton("➕ Add Socket", callback_data='ADD_SOCKET')],
        [InlineKeyboardButton("🔍 Find Socket", callback_data='FIND_SOCKET')],
        [InlineKeyboardButton("❌ Cancel", callback_data="CANCEL")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent = await update.message.reply_text("What would you like to do?", reply_markup=reply_markup)
    context.user_data["messages_to_delete"].append(sent.message_id)
    return rs.CHOOSE_ACTION
