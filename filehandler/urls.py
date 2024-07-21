from django.urls import path
from .views import FileFieldFormView, download_file, get_csrf_token

urlpatterns = [
    path('upload/', FileFieldFormView.as_view(), name='upload'),
    path('download/', download_file, name='download_file'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
]
