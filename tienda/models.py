from django.db import models
from django.contrib.auth.models import User
from juegos.models import Juego

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

class Compra(models.Model):
    ESTADOS = [
        ('PEND', 'Pendiente'),
        ('ENV', 'Enviado'),
        ('ENT', 'Entregado'),
        ('CAN', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    juegos = models.ManyToManyField(Juego, through='DetalleCompra')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=5, choices=ESTADOS, default='PEND')

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
