import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cancion, Historial
from .forms import CancionForm
from django.http import JsonResponse
from .models import Cancion  # Ajusta al nombre real de tu modelo

def canciones_api(request):
    canciones = Cancion.objects.all().values("id", "titulo", "artista", "album", "duracion")
    return JsonResponse(list(canciones), safe=False)

def index(request):
    query = request.GET.get("q")
    canciones_api = []

    # Buscar en iTunes
    if query:
        url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=10"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("results", []):
                canciones_api.append({
                    "titulo": item.get("trackName"),
                    "artista": item.get("artistName"),
                    "cover": item.get("artworkUrl100"),
                    "preview": item.get("previewUrl")
                })

    canciones_locales = Cancion.objects.all()
    form = CancionForm()

    return render(request, "playlist/index.html", {
        "query": query,
        "canciones_api": canciones_api,
        "canciones_locales": canciones_locales,
        "form": form
    })


def add_song(request):
    if request.method == "POST":
        form = CancionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect("index")


def play_song(request, cancion_id):
    cancion = get_object_or_404(Cancion, id=cancion_id)
    Historial.objects.create(cancion=cancion)  # guardar en historial
    return render(request, "playlist/play.html", {"cancion": cancion})
