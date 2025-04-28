import time
from io import BytesIO
from typing import Optional, List
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes
from services.g_drive_service import GDriveService

class GDriveBotService:
    def __init__(self, gdrive_service: GDriveService):
        self.gdrive = gdrive_service
        self.user_images = {}
        
    async def upload_image(self, file_bytes: BytesIO, user_id: int, filename: str = None) -> str:
        if not filename:
            timestamp = int(time.time())
            filename = f"image_{user_id}_{timestamp}.jpg"
        
        result = await self.gdrive.upload_image(file_bytes, filename)
        
        if user_id not in self.user_images:
            self.user_images[user_id] = []
        self.user_images[user_id].append(result['id'])
        
        return result
        
    async def upload_telegram_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        file_id = context.user_data.get("photo_file_id")
        user_id = update.effective_user.id
        file = await context.bot.get_file(file_id)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(file.file_path) as response:
                if response.status == 200:
                    file_content = BytesIO(await response.read())
                    return await self.upload_image(file_content, user_id)
        
        return None
        
    async def get_user_image(self, user_id: int, image_index: int = -1) -> Optional[BytesIO]:
        if user_id not in self.user_images or not self.user_images[user_id]:
            return None
            
        user_files = self.user_images[user_id]
        if abs(image_index) > len(user_files):
            return None
            
        file_id = user_files[image_index]
        
        return await self.gdrive.download_image(file_id)
        
    async def list_user_images(self, user_id: int) -> List[str]:
        return self.user_images.get(user_id, [])
        
    async def delete_user_image(self, user_id: int, image_index: int = -1) -> bool:
        if user_id not in self.user_images or not self.user_images[user_id]:
            return False
            
        user_files = self.user_images[user_id]
        if abs(image_index) > len(user_files):
            return False
            
        file_id = user_files[image_index]
        result = await self.gdrive.delete_image(file_id)
        
        if result:
            self.user_images[user_id].remove(file_id)
            
        return result