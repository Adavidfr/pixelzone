from django.contrib import admin
from .models import Carrito, ItemCarrito, Compra, DetalleCompra

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 0

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_email', 'fecha', 'total')  # Cambié 'usuario' por 'usuario_email'
    inlines = [DetalleCompraInline]

    def usuario_email(self, obj):
        return obj.usuario.email
    usuario_email.short_description = 'Email Usuario'

admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(DetalleCompra)
