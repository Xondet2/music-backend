from django.urls import path
from .views import index, play, upload_file  # Importa solo las vistas necesarias

urlpatterns = [
    path("", index, name="index"),
    path("play/<int:pk>/", play, name="play"),
    path("upload/", upload_file, name="upload"),
]
