import requests
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

def index(request):
    query = request.GET.get("q")
    songs = []
    if query:
        url = f"https://itunes.apple.com/search?term={query}&media=music&limit=10"
        response = requests.get(url).json()
        songs = response.get("results", [])
    return render(request, "playlist/index.html", {"songs": songs})

def play(request, pk):
    # Aquí puedes recuperar canción local o de iTunes
    return render(request, "playlist/play.html")

def upload_file(request):
    if request.method == "POST" and request.FILES["file"]:
        myfile = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        return redirect("index")
    return render(request, "playlist/upload.html")
