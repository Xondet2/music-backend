import requests
from django.http import JsonResponse, HttpResponse
from .models import Cancion, Historial
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # iTunes
    path('buscar/', views.buscar_itunes, name='buscar_itunes'),

    # Playlist
    path('playlist/', views.listar_canciones, name='listar_canciones'),
    path('playlist/agregar/', views.agregar_cancion, name='agregar_cancion'),

    # Reproductor
    path('reproducir/<int:cancion_id>/', views.reproducir, name='reproducir'),
    path('historial/', views.ver_historial, name='ver_historial'),
]

# Home de la app
def index(request):
    return HttpResponse("¡Bienvenido a la página de inicio de Playlist!")

# Buscar canciones en iTunes
def buscar_itunes(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"error": "Falta el parámetro 'q'"}, status=400)

    url = "https://itunes.apple.com/search"
    params = {"term": query, "media": "music", "limit": 10}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return JsonResponse({"error": "No se pudo conectar con iTunes"}, status=500)

    data = response.json()
    resultados = [
        {
            "titulo": track["trackName"],
            "artista": track["artistName"],
            "album": track.get("collectionName", ""),
            "preview": track.get("previewUrl", ""),
        }
        for track in data.get("results", [])
    ]

    return JsonResponse(resultados, safe=False)

# Guardar canción en la base de datos (playlist)
def agregar_cancion(request):
    titulo = request.GET.get("titulo")
    artista = request.GET.get("artista")

    if not titulo or not artista:
        return JsonResponse({"error": "Faltan parámetros"}, status=400)

    cancion = Cancion.objects.create(titulo=titulo, artista=artista)
    return JsonResponse({"id": cancion.id, "titulo": cancion.titulo, "artista": cancion.artista})

# Listar canciones guardadas en la playlist
def listar_canciones(request):
    canciones = list(Cancion.objects.values("id", "titulo", "artista"))
    return JsonResponse(canciones, safe=False)

# Reproducir canción y guardarla en historial
def reproducir(request, cancion_id):
    try:
        cancion = Cancion.objects.get(id=cancion_id)
    except Cancion.DoesNotExist:
        return JsonResponse({"error": "Canción no encontrada"}, status=404)

    Historial.objects.create(cancion=cancion)
    return JsonResponse({"mensaje": f"Reproduciendo {cancion.titulo} - {cancion.artista}"})

# Ver historial de reproducciones
def ver_historial(request):
    historial = Historial.objects.select_related("cancion").order_by("-fecha_reproduccion")
    data = [
        {
            "cancion": h.cancion.titulo,
            "artista": h.cancion.artista,
            "fecha": h.fecha_reproduccion.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for h in historial
    ]
    return JsonResponse(data, safe=False)
