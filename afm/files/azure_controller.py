import uuid
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from django.conf import settings
from . import models

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.svg']

def generate_blob_name(file_name):
    """Generates a unique blob name based on a UUID and file extension."""
    prefix = uuid.uuid4().hex
    ext = Path(file_name).suffix
    return f"{prefix}{ext}"

def upload_file_to_blob(container_name, connection_string, file_content, file_name):
    try:
        blob_name = generate_blob_name(file_name)
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Upload the file content to Azure Blob Storage
        blob_client.upload_blob(file_content, overwrite=True)
        
        return blob_client.url  # Return the URL of the uploaded blob
    except Exception as e:
        # Handle any exceptions here, log them, and possibly raise custom exceptions
        return None  # Or raise an exception depending on your error handling strategy

def check_file_ext(path):
    ext = Path(path).suffix
    return ext in ALLOWED_EXTENSIONS

def list_blobs_in_container(container_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()
        return [blob.name for blob in blob_list]
    except Exception as e:
        # Handle any exceptions here, log them, and possibly raise custom exceptions
        return []

def download_blob(blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=settings.CONTAINER_NAME, blob=blob_name)
        if blob_client.exists():
            blob_content = blob_client.download_blob()
            return blob_content
        else:
            return None
    except Exception as e:
        # Handle any exceptions here, log them, and possibly raise custom exceptions
        return None

def delete_blob(blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=settings.CONTAINER_NAME, blob=blob_name)
        if blob_client.exists():
            blob_client.delete_blob()
        else:
            print("Blob does not exist")
    except Exception as e:
        # Handle any exceptions here, log them, and possibly raise custom exceptions
        print("Failed to delete file")

def save_file_url_to_db(file_path):
    new_file = models.File.objects.create(file_url=file_path)
    new_file.save()
    return new_file
