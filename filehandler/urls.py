from django.urls import path
from .views import FileFieldFormView, download_file

urlpatterns = [
    path('upload/', FileFieldFormView.as_view(), name='upload_file'),
    path('download/', download_file, name='download_file')
]
