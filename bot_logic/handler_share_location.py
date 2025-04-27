import asyncio
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
import bot_logic.return_states as rs


async def share_location_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the location sharing process."""
    keyboard = [
        [KeyboardButton("📍 Share Location", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "📍 Please tap the button below to share your location.",
        reply_markup=reply_markup
    )

    # Start a 30-second timeout in background
    asyncio.create_task(location_timeout(update, context))
    return rs.ASK_FOR_LOCATION

async def location_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Timeout after 30 seconds if no location shared"""
    context.user_data["search_in_progress"] = True
    await asyncio.sleep(30)

    if context.user_data.get("search_in_progress", False):
        await update.message.reply_text(
            "⌛ You didn't share your location in time.\n"
            "If you still want to find the closest spot, please send /search again."
        )