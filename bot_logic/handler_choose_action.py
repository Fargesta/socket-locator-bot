from typing import cast
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import bot_logic.return_states as rs
from db_context import pg_context
from services.g_drive_bot_service import GDriveBotService
from services.socket_locator_service import find_closest_socket

async def handle_choose_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    gdrive_bot = cast(GDriveBotService, context.bot_data["gdrive_bot"])

    if query.data == 'ADD_SOCKET':
        await query.edit_message_text("Please send an image of the socket.")
        return rs.ASK_FOR_IMAGE
    
    elif query.data == 'FIND_SOCKET':
        await query.edit_message_text("Searching for sockets nearby...")

        lat, lon = context.user_data.get("location")
        if lat and lon:

            closest_socket = await find_closest_socket(lat, lon)

            if closest_socket:
                tg_images = await pg_context.get_tg_images_for_location(closest_socket.id)
                tg_image = tg_images[0] if tg_images else None
                if tg_image:
                    image_bytes = await gdrive_bot.get_image_by_id(tg_image.file_id)
                    if image_bytes:
                        image_bytes.seek(0)
                        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_bytes, caption=tg_image.description)

                await context.bot.send_location(latitude=closest_socket.latitude, longitude=closest_socket.longitude, chat_id=update.effective_chat.id)
            else:
                await query.edit_message_text("No sockets found nearby.")
        else:
            await query.edit_message_text("Location not set. Please send your location first.")

        # Call your search logic here
        return ConversationHandler.END
