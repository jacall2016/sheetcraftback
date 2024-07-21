from django.urls import path
from filehandler.views import FileFieldFormView, download_file, get_csrf_token, welcome

urlpatterns = [
    path('', welcome, name='welcome'),
    path('upload/', FileFieldFormView.as_view(), name='upload'),
    path('download/', download_file, name='download'),
    path('csrf_token/', get_csrf_token, name='get_csrf_token'),
]
