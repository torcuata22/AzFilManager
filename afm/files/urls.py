from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name="index"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # path('upload_file/', views.upload_file, name="upload_file"),
    # path('list_files/', views.list_files, name="list_files"),
    # path('download_file/<str:blob_name>/', views.download_file, name="download_file"),
    # path('delete_file/<str:blob_name>/', views.delete_file, name="delete_file"),