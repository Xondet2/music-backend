from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('reproductor.urls')),
    path("", views.index, name="playlist_index"),
    path("buscar/", views.buscar_itunes, name="buscar_itunes"),
    path("agregar/", views.agregar_cancion, name="agregar_cancion"),
    path("canciones/", views.listar_canciones, name="listar_canciones"),
    path("reproducir/<int:cancion_id>/", views.reproducir, name="reproducir"),
    path("historial/", views.ver_historial, name="ver_historial"),
]
