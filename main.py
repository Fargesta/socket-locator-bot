import db_context.pg_context as pg_context
from tortoise import run_async
import logging
import bot_logic.tg_bot as tg_bot
from file_context.g_drive_bot_service import TelegramGDriveBot
import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def gdrive_bot_start(application) -> None:
    service_account_file = settings.DRIVE_KEY_PATH
    drive_folder_id = settings.DRIVE_FOLDER_ID
    
    gdrive_bot = TelegramGDriveBot(service_account_file, drive_folder_id)
    await gdrive_bot.initialize()
    
    application.bot_data["gdrive_bot"] = gdrive_bot

def main() -> None:
    run_async(pg_context.init_db())
    print("Database initialized successfully.")
    tg_bot.bot_start()

if __name__ == "__main__":
    main()