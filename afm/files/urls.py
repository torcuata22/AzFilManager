from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('list_files/', views.list_files, name="list_files"),
    path('download_file/<str:blob_name>/', views.download_file, name="download_file"),
    path('delete_file/<str:blob_name>/', views.delete_file, name="delete_file"),
    path('accounts/', include('django.contrib.auth.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
