from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot_logic.handler_cancel import cancel_command
import bot_logic.return_states as rs

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo
    if not photo:
        await update.message.reply_text("❌ No photo found. Please send a photo.")
        await cancel_command(update, context)
    
    context.user_data["photo_file_id"] = photo[-1].file_id

    caption = update.message.caption
    if caption:
        context.user_data["photo_caption"] = caption

    context.user_data["messages_to_delete"].append(update.message.message_id)

    keyboard = [
        [InlineKeyboardButton("220V 2 Pin", callback_data="220V"), InlineKeyboardButton("380V 4 Pin", callback_data="4PIN")],
        [InlineKeyboardButton("380V 5 Pin", callback_data="5PIN"), InlineKeyboardButton("Unknown", callback_data="UNKN")],
        [InlineKeyboardButton("❌ Cancel", callback_data="CANCEL")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sent = await update.message.reply_text("Please select socket type:", reply_markup=reply_markup)
    context.user_data['messages_to_delete'] = [update.message.message_id, sent.message_id]

    return rs.ASK_FOR_TYPE