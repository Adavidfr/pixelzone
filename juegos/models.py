from django.db import models

class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_miniatura = models.URLField(null=True, blank=True)
    imagen_principal = models.URLField(null=True, blank=True)
    imagen2 = models.URLField(null=True, blank=True)
    imagen3 = models.URLField(null=True, blank=True)
    imagen4 = models.URLField(null=True, blank=True)
    imagen5 = models.URLField(null=True, blank=True)
    video = models.URLField(null=True, blank=True)    
    descripcion = models.TextField()
    fecha_lanzamiento = models.DateField()
    desarrollador = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    descuento = models.IntegerField()

    def __str__(self):
        return self.nombre