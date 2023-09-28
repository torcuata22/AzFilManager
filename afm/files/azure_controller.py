from io import BytesIO
import environ
import uuid
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient, BlobServiceClient #BlobClient(account_url: str, container_name: str, blob_name: str,
from django.conf import settings

from . import models


ALLOWED_EXTENSIONS = ['.png', '.jpg', '.svg',]

def check_file_ext(path):
    ext = Path(path).suffix
    return ext in ALLOWED_EXTENSIONS

def list_blobs():
    blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container = settings.CONTAINER_NAME, blob='blob_name')
    container_name=settings.CONTAINER_NAME
    container_client=blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(container_name)
    for blob in blob_list:
        blob_name = blob.name
        return blob_name
    return blob_list
    
    
def download_a_blob(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container = settings.CONTAINER_NAME, blob=blob_name)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content


def delete_a_blob(blob_name):
     blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
     container_client = blob_service_client.get_blob_client(container = settings.CONTAINER_NAME, blob=blob_name)
     try:
        if container_client.exists():
            container_client.delete_blob()
        else:
            print("Blob does not exist")
     except Exception as e:
         print("Failed to delete file")
    
def save_file_url_to_db(file_url):
    new_file = models.File.objects.create(file_url = file_url)
    new_file.save()
    return new_file

def upload_file_to_blob(file_path, file_name):
    prefix = uuid.uuid4().hex
    ext=Path(file_name).suffix
    file_url=f'{prefix}{ext}'
    blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container = settings.CONTAINER_NAME, blob=file_name)
    blob_client.upload_blob(file_path, overwrite=True)
    save_file_url_to_db(blob_client.url)
    print(f"Uploaded {file_name}")

    
   
