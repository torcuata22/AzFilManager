from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .azure_controller import ALLOWED_EXTENSIONS,  upload_file_to_blob, download_a_blob, delete_a_blob, list_blobs
from azure.storage.blob import BlobServiceClient, ContainerClient
from uuid import uuid4

from . import models
from .models import File

from hashlib import new
from pathlib import Path
import mimetypes


# Create your views here.

def index(request):
    return render (request, 'files/index.html')

def list_files(request):
    blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
    container_name=settings.CONTAINER_NAME
    container_client=blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    #for paginator (b/c Azure object not iterable):
    blob_name_list=[]
    for blob in blob_list:
        blob_name = blob.name
        blob_name_list.append(blob_name)
    paginator = Paginator(blob_name_list, 10)  #Change number of items per page to a higher number (10? 20?)
    page = request.GET.get('page') 
    blob_name_list = paginator.get_page(page)
    
  

    return render(request, 'files/list_files.html', {'blob_name_list': blob_name_list})

def upload_file(request):
    if request.method == "POST": 
        files = request.FILES.getlist('files')
        for file in files:
            file_name = file.name
            upload_file_to_blob(file, file_name)    
            messages.success(request, f"{file.name} was successfully uploaded")
    return render(request, 'files/upload_file.html', {})


def delete_file(request,blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING)
    container_name=settings.CONTAINER_NAME
    container_client=blob_service_client.get_container_client(container_name)
    blob_list=list_blobs()
    for blob in blob_list:
        blob_name = blob.name
    delete_a_blob(blob_name)
    list_blobs()
    return render(request,'files/delete_file.html', {"blob_list":blob_list})   #(request,"files/delete_file.html", {'file_id': file_id})


    #NOT WORKING YET:

def download_file(request, blob_name):
    blob_content = download_a_blob(blob_name)
    if blob_content:
        response = HttpResponse(blob_content.readall())
        response['Content-Disposition'] = f'attachment; filename={blob_name}'
        messages.success(request, "Your file was successfully downloaded")
        return response
    return render(request, 'files/list_files.html', {})