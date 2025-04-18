from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    messages = context.user_data.get("messages_to_delete", [])
    for message_id in messages:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            print(f"Failed to delete message {message_id}: {e}")

    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    except Exception as e:
        print(f"Couldn't delete /cancel command: {e}")

    context.user_data.clear()

    await update.message.reply_text('New location canceled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
