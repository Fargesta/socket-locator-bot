from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import bot_logic.return_states as rs

async def handle_choose_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'ADD_SOCKET':
        await query.edit_message_text("Please send an image of the socket.")
        return rs.ASK_FOR_IMAGE
    elif query.data == 'FIND_SOCKET':
        await query.edit_message_text("Searching for sockets nearby...")
        # Call your search logic here
        return ConversationHandler.END
