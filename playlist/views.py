import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Cancion, Historial
import cloudinary
import cloudinary.uploader
from datetime import timedelta

# Configurar Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

def index(request):
    query = request.GET.get("q")
    itunes_songs = []
    
    # Buscar en iTunes si hay query
    if query:
        url = f"https://itunes.apple.com/search?term={query}&media=music&limit=10"
        response = requests.get(url).json()
        itunes_songs = response.get("results", [])
    
    # Obtener canciones locales subidas
    local_songs = Cancion.objects.all()
    
    return render(request, "playlist/index.html", {
        "itunes_songs": itunes_songs,
        "local_songs": local_songs,
        "query": query
    })

def play(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)
    
    # Registrar en historial
    Historial.objects.create(cancion=cancion)
    
    return render(request, "playlist/play.html", {"cancion": cancion})

def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        myfile = request.FILES["file"]
        artista = request.POST.get("artista", "Desconocido")
        
        # Validar tamaño del archivo (máximo 10MB)
        max_size = 10 * 1024 * 1024  # 10 MB en bytes
        if myfile.size > max_size:
            return render(request, "playlist/upload.html", {
                "error": f"El archivo es demasiado grande. Máximo permitido: 10MB. Tu archivo: {myfile.size / (1024*1024):.1f}MB"
            })
        
        try:
            # Subir a Cloudinary
            upload_result = cloudinary.uploader.upload(
                myfile,
                resource_type="video",  # Para archivos de audio
                folder="music_uploads"
            )
            
            # Obtener duración si está disponible
            duracion_segundos = upload_result.get('duration', 0)
            duracion = timedelta(seconds=int(duracion_segundos)) if duracion_segundos else None
            
            # Guardar en base de datos
            Cancion.objects.create(
                titulo=myfile.name.rsplit('.', 1)[0],  # Nombre sin extensión
                artista=artista,
                archivo=upload_result['secure_url'],
                cloudinary_id=upload_result.get('public_id'),
                duracion=duracion
            )
            
            return redirect("index")
            
        except Exception as e:
            return render(request, "playlist/upload.html", {
                "error": f"Error al subir el archivo: {str(e)}"
            })
    
    return render(request, "playlist/upload.html")