from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # Agregado para servir plantillas
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("playlist/", include("playlist.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),  # Agregado: Ruta para el frontend
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
