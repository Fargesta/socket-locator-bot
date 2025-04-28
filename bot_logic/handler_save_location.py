from bot_logic.type_converter import type_to_name
from telegram.ext import ContextTypes, ConversationHandler
import db_context.pg_context as pg_context
from telegram import Update
from file_context.g_drive_bot_service import GDriveBotService
from typing import cast
import settings

UPLOAD_FOLDER_URL = f'https://drive.google.com/drive/folders/{settings.DRIVE_FOLDER_ID}'

async def handle_save_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = None
    query = update.callback_query
    await query.answer()

    gdrive_bot = cast(GDriveBotService, context.bot_data["gdrive_bot"])

    try:
        user = await pg_context.get_tg_user(update.effective_user.id)
        if not user:
            await query.message.reply_text("❌ User not found. Cannot save.")
            raise Exception("User not found in the database.")
        
        upload = await gdrive_bot.upload_telegram_photo(update, context)
        if not upload:
            await query.message.reply_text("❌ Failed to upload image. Cannot save.")
            raise Exception("Failed to upload image.")
        
        lat, lon = context.user_data.get("location")
        sc_type = context.user_data.get("selected_type")
        location = await pg_context.create_tg_location(
            latitude=lat,
            longitude=lon,
            name=type_to_name(sc_type),
            socket_type=sc_type,
            description=context.user_data.get("description"),
            created_by=user
        )

        await pg_context.create_tg_image(
            url=UPLOAD_FOLDER_URL,
            file_size=cast(int, upload["size"]),
            file_id=upload["id"],
            location=location,
            file_saved=True,
            file_name=upload["name"],
            description=context.user_data.get("photo_caption"),
            created_by=user
        )

        context.user_data["messages_to_delete"].append(query.message.message_id)
        msg = await query.message.reply_text("✅ Location saved successfully!")
        context.user_data["messages_to_delete"].append(msg.message_id)
        
    except Exception as e:
        print(f"Something went wrong: {e}")
    finally:
        await pg_context.close_db()
        return ConversationHandler.END
