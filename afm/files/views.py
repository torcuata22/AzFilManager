from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from azure.storage.blob import BlobServiceClient
from uuid import uuid4

from . import models
from .models import File
from .azure_controller import (
    ALLOWED_EXTENSIONS,
    upload_file_to_blob,
    download_blob,
    delete_blob,
    list_blobs_in_container,
)

def index(request):
    """
    Render the index page.
    """
    return render(request, 'files/index.html')

def list_files(request):
    """
    List files from Azure Blob Storage and paginate the results.
    """
    blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
    container_name = settings.CONTAINER_NAME
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = list_blobs_in_container()
    
    paginator = Paginator(blob_list, 10)  # Change the number of items per page as needed
    page = request.GET.get('page') 
    blob_name_list = paginator.get_page(page)
  
    return render(request, 'files/list_files.html', {'blob_name_list': blob_name_list})

def upload_file(request):
    """
    Handle file upload to Azure Blob Storage.
    """
    if request.method == "POST": 
        files = request.FILES.getlist('files')
        for file in files:
            file_name = file.name
            upload_file_to_blob(file, file_name)    
            messages.success(request, f"{file_name} was successfully uploaded")
    return render(request, 'files/upload_files.html', {})

def delete_file(request, blob_name):
    """
    Delete a file from Azure Blob Storage.
    """
    try:
        delete_blob(blob_name)
        messages.success(request, f"{blob_name} was successfully deleted")
    except Exception as e:
        messages.error(request, f"Failed to delete {blob_name}: {str(e)}")

    return render(request, 'files/delete_file.html', {})

def download_file(request, blob_name):
    """
    Download a file from Azure Blob Storage.
    """
    blob_content = download_blob(blob_name)
    if blob_content:
        response = HttpResponse(blob_content.readall())
        response['Content-Disposition'] = f'attachment; filename={blob_name}'
        messages.success(request, "Your file was successfully downloaded")
        return response
    
    return render(request, 'files/list_files.html', {})
