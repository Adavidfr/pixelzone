from django.db import models

class Juego(models.Model):
    appid = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.URLField()
    descripcion = models.TextField()
    fecha_lanzamiento = models.DateField()
    desarrollador = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    descuento = models.IntegerField()
    es_gratis = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre