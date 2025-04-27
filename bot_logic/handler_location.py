from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
import bot_logic.return_states as rs        

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    context.user_data["location"] = (location.latitude, location.longitude)
    context.user_data["messages_to_delete"] = [update.message.message_id]

    keyboard = [
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ]
    sent = await update.message.reply_text(
        "📸 Please send a photo of this location.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    context.user_data["messages_to_delete"].append(sent.message_id)
    return rs.ASK_FOR_IMAGE