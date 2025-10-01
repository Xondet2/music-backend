from django.db import models

class Cancion(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100)
    duracion = models.DurationField(null=True, blank=True)
    # Cambiado de FileField a URLField para Cloudinary
    archivo = models.URLField(max_length=500, null=True, blank=True)
    # Agregamos campos útiles
    cloudinary_id = models.CharField(max_length=200, null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.artista}"

    class Meta:
        ordering = ['-fecha_subida']
        verbose_name_plural = "Canciones"


class Historial(models.Model):
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    fecha_reproduccion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cancion.titulo} reproducida el {self.fecha_reproduccion.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-fecha_reproduccion']
        verbose_name_plural = "Historial"