import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# Path to your service account key JSON file (replace with your actual path)
SERVICE_ACCOUNT_KEY_PATH = '/path/to/your/service_account_key.json'

# Define the scope for Google Drive access
SCOPES = ['https://www.googleapis.com/auth/drive.file']

async def _get_drive_service_async():
    """Asynchronously gets the Google Drive API service using a service account."""
    if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
        raise ValueError(
            f"Service account key file not found at: {SERVICE_ACCOUNT_KEY_PATH}.  Ensure SERVICE_ACCOUNT_KEY_PATH is set correctly."
        )
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_KEY_PATH, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

async def upload_image_to_drive_async(folder_id, image_path, filename):
    """Asynchronously uploads an image to a specific folder in Google Drive using a service account."""
    try:
        service = await _get_drive_service_async()

        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(image_path, mimetype='image/jpeg')  # Adjust mimetype as needed

        file = await service.files().create(body=file_metadata,
                                            media=media,
                                            fields='id').execute_async()  # Use execute_async
        print(f'File ID: {file.get("id")} uploaded to folder: {folder_id}')
        return file.get("id")

    except HttpError as error:
        print(f'An error occurred during upload: {error}')
        return None

async def download_file_from_drive_async(file_id, save_path):
    """Asynchronously downloads a file from Google Drive using its file ID and a service account."""
    try:
        service = await _get_drive_service_async()

        file_metadata = await service.files().get(fileId=file_id, fields='name').execute_async()
        file_name = file_metadata.get('name')
        full_save_path = os.path.join(save_path, file_name)

        request = service.files().get_media(fileId=file_id)
        fh = open(full_save_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request, chunksize=4 * 1024 * 1024)  # Increase chunksize
        done = False
        while done is False:
            status, done = await downloader.next_chunk()  # Await the next chunk
            if status:
                print(f"Download Progress for '{file_name}': {int(status.progress() * 100)}%")

        print(f"File '{file_name}' downloaded to '{full_save_path}'")
        return full_save_path

    except HttpError as error:
        print(f'An error occurred during download: {error}')
        return None

# Example of how to call these functions from another module:
#
# async def main_caller():
#     folder_id = 'your_folder_id'
#     image_path = '/path/to/your/local/image.jpg'
#     upload_filename = 'uploaded_from_module.jpg'
#     download_file_id = 'your_file_id_to_download'
#     download_directory = '/path/to/your/download/directory/from_module'
#
#     if not os.path.exists(download_directory):
#         os.makedirs(download_directory)
#
#     uploaded_file_id = await upload_image_to_drive_async(folder_id, image_path, upload_filename)
#     if uploaded_file_id:
#         print(f"Upload from module successful. File ID: {uploaded_file_id}")
#
#     if download_file_id:
#         downloaded_file_path = await download_file_from_drive_async(download_file_id, download_directory)
#         if downloaded_file_path:
#             print(f"Download from module successful. File saved to: {downloaded_file_path}")
#
# if __name__ == "__main__":
#     asyncio.run(main_caller())