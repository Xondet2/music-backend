from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("play/<int:pk>/", views.play, name="play"),
    path("upload/", views.upload_file, name="upload"),
]
