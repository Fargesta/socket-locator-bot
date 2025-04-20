from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.setdefault("messages_to_delete", []).append(query.message.message_id)

    chat_id = query.message.chat_id
    for msg_id in context.user_data["messages_to_delete"]:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print(f"Failed to delete message {msg_id}: {e}")

    return ConversationHandler.END

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.setdefault("messages_to_delete", []).append(update.message.message_id)
    chat_id = update.effective_chat.id

    for msg_id in context.user_data["messages_to_delete"]:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print(f"Failed to delete message {msg_id}: {e}")

    return ConversationHandler.END