from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views import generic
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
    save_file_url_to_db,
)
from .forms import UserRegistrationForm



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
    blob_list = list_blobs_in_container(container_name=container_name)
    paginator = Paginator(blob_list, 5)  # Change the number of items per page as needed
    page = request.GET.get('page') 
    blob_name_list = paginator.get_page(page)
    
    return render(request, 'files/list_files.html', {'blob_name_list': blob_name_list})

def upload_file(request):
    """
    Handle file upload to Azure Blob Storage.
    """
   
    if request.method == "POST": 
        files = request.FILES.getlist('files')
        container_name = settings.CONTAINER_NAME
        connection_string = settings.CONNECTION_STRING
        for file in files:
            file_name = file.name
            file_content = file.read()
            print(f"Uploading file: {file_name}")
            print(f"Container Name: {container_name}")
            print(f"Connection String: {connection_string}")
            result = upload_file_to_blob(container_name, connection_string, file_content, file_name)
            print(f"Upload Result: {result}")
            if result:
                messages.success(request, f"{file_name} was successfully uploaded")
                print(f"File uploaded successfully. URL: {result}")
                # Save the file URL to the database
                save_file_url_to_db(result)
            else:
                messages.error(request, f"Failed to upload {file_name}")
                print(f"Failed to upload {file_name}")
                return HttpResponseServerError("Failed to upload the file to Azure Blob Storage.")
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

#AUTHENTICATION:
@login_required
class IndexListView(ListView):
    model = User
    template_name = "registration/login.html"
    context_object_name = "users"


class RegistrationView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! You can now log in.')
        return response
    

@login_required        
def logout_user(request):
    logout(request)
    messages.success(request, "You've been succesfully logged out")
    return redirect("login")