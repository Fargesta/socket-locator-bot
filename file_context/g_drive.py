from services.g_drive_bot_service import GDriveBotService
from services.g_drive_service import GDriveService
from telegram.ext import Application
import settings

async def gdrive_bot_start(app: Application) -> None:
    service_account_file = settings.DRIVE_KEY_PATH
    drive_folder_id = settings.DRIVE_FOLDER_ID
    
    gdrive_service = GDriveService(service_account_file, drive_folder_id)
    gdrive_bot = GDriveBotService(gdrive_service)
    
    app.bot_data["gdrive_bot"] = gdrive_bot