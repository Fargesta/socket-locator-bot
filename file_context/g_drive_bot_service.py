from io import BytesIO
from g_drive_service import GoogleDriveService
from telegram import Update
from telegram.ext import ContextTypes
import aiohttp

class TelegramGDriveBot:
    """
    Telegram bot module for handling image uploads and downloads with Google Drive.
    """
    
    def __init__(self, service_account_file: str, drive_folder_id: str):
        """
        Initialize the Telegram Google Drive bot.
        
        Args:
            service_account_file: Path to the service account JSON key file
            drive_folder_id: ID of the Google Drive folder to use
        """
        self.gdrive = GoogleDriveService(service_account_file, drive_folder_id)
        # Dictionary to store user image mappings (user_id -> [file_ids])
        self.user_images = {}
        
    async def initialize(self):
        """Initialize the Google Drive service."""
        await self.gdrive.initialize_service()
        
    async def handle_image_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
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
        
        # Get file from Telegram
        file = await context.bot.get_file(photo.file_id)
        
        # Download the file to BytesIO
        async with aiohttp.ClientSession() as session:
            async with session.get(file.file_path) as response:
                if response.status == 200:
                    file_content = BytesIO(await response.read())
                    
                    # Generate a unique filename
                    user_id = update.effective_user.id
                    timestamp = context.bot.get_me().date.timestamp()
                    filename = f"image_{user_id}_{timestamp}.jpg"
                    
                    # Upload to Google Drive
                    file_id = await self.gdrive.upload_image(file_content, filename)
                    
                    # Store the file ID for the user
                    if user_id not in self.user_images:
                        self.user_images[user_id] = []
                    self.user_images[user_id].append(file_id)
                    
                    return file_id
        
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


# Example usage in a Telegram bot handler (not to be included in the module)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Example handler for photo messages."""
    # Access the bot from context
    gdrive_bot = context.bot_data["gdrive_bot"]
    
    # Upload the image
    file_id = await gdrive_bot.handle_image_upload(update, context)
    
    # Send a confirmation message
    if file_id:
        await update.message.reply_text(f"Image uploaded successfully! ID: {file_id}")
    else:
        await update.message.reply_text("Failed to upload image.")


async def handle_get_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Example handler for retrieving images."""
    # Access the bot from context
    gdrive_bot = context.bot_data["gdrive_bot"]
    
    # Get the user's latest image
    user_id = update.effective_user.id
    image_data = await gdrive_bot.get_user_image(user_id)
    
    # Send the image back to the user
    if image_data:
        await update.message.reply_photo(image_data)
    else:
        await update.message.reply_text("No images found for you.")