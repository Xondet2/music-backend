from django.db import models

class Cancion(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100)
    duracion = models.DurationField(null=True, blank=True)
    archivo = models.FileField(upload_to="canciones/", null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.artista}"


class Historial(models.Model):
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    fecha_reproduccion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cancion.titulo} reproducida el {self.fecha_reproduccion.strftime('%Y-%m-%d %H:%M')}"
