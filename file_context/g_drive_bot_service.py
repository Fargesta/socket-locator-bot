import time
from io import BytesIO
from typing import Optional, List
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes
from file_context.g_drive_service import GDriveService

class GDriveBotService:
    """
    Telegram bot module for handling image uploads and downloads with Google Drive.
    """
    
    def __init__(self, gdrive_service: GDriveService):
        """
        Initialize the Telegram Google Drive bot.
        
        Args:
            gdrive_service: GDriveService instance for Drive operations
        """
        self.gdrive = gdrive_service
        # Dictionary to store user image mappings (user_id -> [file_ids])
        self.user_images = {}
        
    async def upload_image(self, file_bytes: BytesIO, user_id: int, filename: str = None) -> str:
        """
        Upload an image to Google Drive.
        
        Args:
            file_bytes: BytesIO object containing the image
            user_id: Telegram user ID
            filename: Optional filename (generates one if not provided)
            
        Returns:
            File ID of the uploaded image
        """
        # Generate filename if not provided
        if not filename:
            timestamp = int(time.time())
            filename = f"image_{user_id}_{timestamp}.jpg"
        
        # Upload to Google Drive
        file_id = await self.gdrive.upload_image(file_bytes, filename)
        
        # Store the file ID for the user
        if user_id not in self.user_images:
            self.user_images[user_id] = []
        self.user_images[user_id].append(file_id)
        
        return file_id
        
    async def upload_telegram_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """
        Handle image upload from Telegram user.
        
        Args:
            update: Telegram update object
            context: Telegram context object
            
        Returns:
            File ID of the uploaded image
        """
        # Get the photo with the highest resolution
        photo = update.message.photo[-1]
        user_id = update.effective_user.id
        
        # Get file from Telegram
        file = await context.bot.get_file(photo.file_id)
        
        # Download the file to BytesIO
        async with aiohttp.ClientSession() as session:
            async with session.get(file.file_path) as response:
                if response.status == 200:
                    file_content = BytesIO(await response.read())
                    return await self.upload_image(file_content, user_id)
        
        return None
        
    async def get_user_image(self, user_id: int, image_index: int = -1) -> Optional[BytesIO]:
        """
        Get a specific image for a user.
        
        Args:
            user_id: Telegram user ID
            image_index: Index of the image to retrieve (-1 for the latest)
            
        Returns:
            BytesIO object containing the image data, or None if not found
        """
        if user_id not in self.user_images or not self.user_images[user_id]:
            return None
            
        # Get the file ID for the requested image
        user_files = self.user_images[user_id]
        if abs(image_index) > len(user_files):
            return None
            
        file_id = user_files[image_index]
        
        # Download the image from Google Drive
        return await self.gdrive.download_image(file_id)
        
    async def list_user_images(self, user_id: int) -> List[str]:
        """
        List all image IDs for a specific user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            List of file IDs belonging to the user
        """
        return self.user_images.get(user_id, [])
        
    async def delete_user_image(self, user_id: int, image_index: int = -1) -> bool:
        """
        Delete a specific image for a user.
        
        Args:
            user_id: Telegram user ID
            image_index: Index of the image to delete (-1 for the latest)
            
        Returns:
            True if successful, False otherwise
        """
        if user_id not in self.user_images or not self.user_images[user_id]:
            return False
            
        # Get the file ID for the requested image
        user_files = self.user_images[user_id]
        if abs(image_index) > len(user_files):
            return False
            
        file_id = user_files[image_index]
        
        # Delete the image from Google Drive
        result = await self.gdrive.delete_image(file_id)
        
        # If successful, remove from user images
        if result:
            self.user_images[user_id].remove(file_id)
            
        return result