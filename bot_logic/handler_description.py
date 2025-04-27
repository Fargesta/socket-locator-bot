from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import bot_logic.return_states as rs

async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        # User pressed "Skip"
        query = update.callback_query
        await query.answer()
        description = None
        context.user_data["messages_to_delete"].append(query.message.message_id)
    else:
        # User typed a description
        message = update.message
        description = message.text
        context.user_data["messages_to_delete"].append(message.message_id)

    context.user_data["description"] = description

    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data="CONFIRM")],
        [InlineKeyboardButton("❌ Cancel", callback_data="CANCEL")]
    ]

    summary = (
        f"📍 Location: {context.user_data.get('location')}\n"
        f"🅿️ Option: {context.user_data.get('selected_type')}\n"
        f"📝 Description: {description if description else 'Skipped'}"
    )

    msg = await (query.message if update.callback_query else message).reply_text(
        "Please confirm to save:\n\n" + summary,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    context.user_data["messages_to_delete"].append(msg.message_id)

    return rs.CONFIRM_SAVE