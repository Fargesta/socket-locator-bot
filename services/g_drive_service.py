import asyncio
from io import BytesIO
from typing import Optional, Tuple, List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

class GDriveService:
    def __init__(self, service_account_file: str, folder_id: str):
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
            lambda: build('drive', 'v3', credentials=self.credentials, cache_discovery=False)
        )
        
    async def upload_image(self, file_bytes: BytesIO, filename: str) -> str:
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
            fields='id, name, size'
        )
        
        response = await loop.run_in_executor(None, request.execute)
        return {
            'id': response.get('id'),
            'name': response.get('name'),
            'size': int(response.get('size', 0))  # 'size' comes as a string, so cast to int
        }
    
    async def download_image(self, file_id: str) -> BytesIO:
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