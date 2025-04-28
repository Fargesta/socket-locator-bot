from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot_logic.handler_cancel import cancel_callback
import bot_logic.return_states as rs

async def handle_socket_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    if callback_data == "CANCEL":
        await cancel_callback(update, context)

    context.user_data['selected_type'] = callback_data
    context.user_data['messages_to_delete'].append(query.message.message_id)

    keyboard = [
        [InlineKeyboardButton("⏭️ Skip", callback_data="SKIP")], [InlineKeyboardButton("❌ Cancel", callback_data="CANCEL")]
    ]

    msg = await query.message.reply_text("Please provide a description for the location:", reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data['messages_to_delete'].append(msg.message_id)

    return rs.ASK_FOR_DESCRIPTION
