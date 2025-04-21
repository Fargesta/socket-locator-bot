from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
import db_context.pg_context as pg_context
from bot_logic.handler_cancel import cancel_callback

ASK_FOR_TYPE, ASK_FOR_DESCRIPTION, ASK_FOR_IMAGE = range(3)

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
    return ASK_FOR_IMAGE


async def ask_for_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo
    if not photo:
        return
    
    context.user_data["photo_file_id"] = photo[-1].file_id
    context.user_data["messages_to_delete"].append(update.message.message_id)

    keyboard = [
        [InlineKeyboardButton("220V 2 Pin", callback_data="220V"), InlineKeyboardButton("380V 4 Pin", callback_data="4PIN")],
        [InlineKeyboardButton("380V 5 Pin", callback_data="5PIN"), InlineKeyboardButton("Unknown", callback_data="UNKN")],
        [InlineKeyboardButton("❌ Cancel", callback_data="CANCEL")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sent = await update.message.reply_text("Please select socket type:", reply_markup=reply_markup)
    context.user_data['messages_to_delete'] = [update.message.message_id, sent.message_id]

    return ASK_FOR_TYPE


async def ask_for_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    if callback_data == "CANCEL":
        await cancel_callback(update, context)

    context.user_data['selected_type'] = callback_data
    context.user_data['messages_to_delete'].append(query.message.message_id)

    keyboard = [
        [InlineKeyboardButton("⏭️ Skip", callback_data="SKIP")], [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]

    msg = await query.message.reply_text("Please provide a description for the location:", reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data['messages_to_delete'].append(msg.message_id)

    return ASK_FOR_DESCRIPTION


async def ask_for_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    context.user_data["description"] = text
    context.user_data["messages_to_delete"].append(update.message.message_id)

    summary = (
        f"✅ Please confirm!\n\n"
        f"📍 Location: {context.user_data.get('location')}\n"
        f"🅿️ Option: {context.user_data.get('selected_type')}\n"
        f"📝 Description: {text}"
    )
    msg = await update.message.reply_text(summary)
    context.user_data["messages_to_delete"].append(msg.message_id)

    return ConversationHandler.END


async def skip_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data["description"] = None
    context.user_data["messages_to_delete"].append(query.message.message_id)

    summary = (
        f"✅ Please confirm!\n\n"
        f"📍 Location: {context.user_data.get('location')}\n"
        f"🅿️ Option: {context.user_data.get('selected_type')}\n"
        f"📝 Description: Skipped"
    )
    msg = await query.message.reply_text(summary)
    context.user_data["messages_to_delete"].append(msg.message_id)

    return ConversationHandler.END