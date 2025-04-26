import asyncio
from io import BytesIO
from typing import Optional, Tuple, List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

class GDriveService:
    """
    Asynchronous Google Drive manager for handling file operations.
    """
    
    def __init__(self, service_account_file: str, folder_id: str):
        """
        Initialize the Google Drive manager with service account credentials.
        
        Args:
            service_account_file: Path to the service account JSON key file
            folder_id: ID of the Google Drive folder to use for file storage
        """
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.folder_id = folder_id
        self.service = None
        
    async def initialize_service(self):
        """Initialize the Google Drive service in an async context."""
        loop = asyncio.get_event_loop()
        self.service = await loop.run_in_executor(
            None,
            lambda: build('drive', 'v3', credentials=self.credentials)
        )
        
    async def upload_image(self, file_bytes: BytesIO, filename: str) -> str:
        """
        Upload an image to Google Drive.
        
        Args:
            file_bytes: BytesIO object containing the image data
            filename: Name to save the file as
            
        Returns:
            File ID of the uploaded image
        """
        if not self.service:
            await self.initialize_service()
            
        file_bytes.seek(0)  # Reset file pointer to beginning
        
        file_metadata = {
            'name': filename,
            'parents': [self.folder_id]
        }
        
        media = MediaIoBaseUpload(
            file_bytes, 
            mimetype='image/jpeg',
            resumable=True
        )
        
        loop = asyncio.get_event_loop()
        request = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        )
        
        response = await loop.run_in_executor(None, request.execute)
        return response.get('id')
        
    async def download_image(self, file_id: str) -> BytesIO:
        """
        Download an image from Google Drive.
        
        Args:
            file_id: ID of the file to download
            
        Returns:
            BytesIO object containing the downloaded image
        """
        if not self.service:
            await self.initialize_service()
            
        file_bytes = BytesIO()
        request = self.service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(file_bytes, request)
        
        loop = asyncio.get_event_loop()
        done = False
        while not done:
            status, done = await loop.run_in_executor(None, downloader.next_chunk)
        
        file_bytes.seek(0)  # Reset file pointer to beginning
        return file_bytes
        
    async def list_images(self, limit: int = 10) -> List[Tuple[str, str]]:
        """
        List images stored in the Google Drive folder.
        
        Args:
            limit: Maximum number of images to return
            
        Returns:
            List of tuples containing (file_id, file_name)
        """
        if not self.service:
            await self.initialize_service()
            
        query = f"'{self.folder_id}' in parents and trashed = false"
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=limit
            ).execute()
        )
        
        files = response.get('files', [])
        return [(file['id'], file['name']) for file in files]
        
    async def get_image_by_name(self, filename: str) -> Optional[str]:
        """
        Find an image by its filename.
        
        Args:
            filename: Name of the file to find
            
        Returns:
            File ID if found, None otherwise
        """
        if not self.service:
            await self.initialize_service()
            
        query = f"name = '{filename}' and '{self.folder_id}' in parents and trashed = false"
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id)'
            ).execute()
        )
        
        files = response.get('files', [])
        return files[0]['id'] if files else None
        
    async def delete_image(self, file_id: str) -> bool:
        """
        Delete an image from Google Drive.
        
        Args:
            file_id: ID of the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            await self.initialize_service()
            
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.service.files().delete(fileId=file_id).execute()
            )
            return True
        except Exception:
            return False