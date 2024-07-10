from django.urls import path
from .views import FileFieldFormView, download_file, get_csrf_token

urlpatterns = [
    path('upload/', FileFieldFormView.as_view(), name='file-upload'),
    path('download/', download_file, name='file-download'),
    path('csrf-token/', get_csrf_token, name='csrf-token'),
]