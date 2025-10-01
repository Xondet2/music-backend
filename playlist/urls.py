from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path("api/canciones/", views.canciones_api, name="canciones_api"),
    path("", views.index, name="index"),
    path("add_song/", views.add_song, name="add_song"),
    path("play/<int:cancion_id>/", views.play_song, name="play_song"),
]
