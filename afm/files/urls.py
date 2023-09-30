from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import RegistrationView


urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login')), name='index'),
    path('index/', views.index, name="index"),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('list_files/', views.list_files, name="list_files"),
    path('download_file/<str:blob_name>/', views.download_file, name="download_file"),
    path('delete_file/<str:blob_name>/', views.delete_file, name="delete_file"),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(), name='login' ),
    path('logout/', views.logout_user, name='logout' ),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
