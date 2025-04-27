import asyncio
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
import bot_logic.return_states as rs


async def handle_share_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the location sharing process."""
    keyboard = [
        [KeyboardButton("📍 Share Location", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "📍 Please tap the button below to share your location.",
        reply_markup=reply_markup
    )

    # ✅ Save timeout task inside user_data
    timeout_task = asyncio.create_task(location_timeout(update, context))
    context.user_data["search_timeout_task"] = timeout_task

    return rs.ASK_FOR_LOCATION

async def location_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Timeout after 30 seconds if no location shared"""
    try:
        await asyncio.sleep(30)

        await update.message.reply_text(
            "⌛ You didn't share your location in time.\n"
            "If you still want to find or add socket, please repeat command."
        )
    except asyncio.CancelledError:
        # ✅ Task was canceled because user shared location → silently ignore
        pass