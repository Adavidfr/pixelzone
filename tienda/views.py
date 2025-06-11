from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from django.db import models

from .models import Carrito, ItemCarrito, Compra, DetalleCompra
from juegos.models import Juego

# -----------------------------
# FUNCIONES PARA USUARIOS AUTENTICADOS
# -----------------------------

@login_required
def agregar_al_carrito(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, juego=juego)

    if not creado:
        item.cantidad += 1
        item.save()

    messages.success(request, f"{juego.nombre} agregado al carrito.")
    return redirect('lista_juegos')


@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related('juego')
    total = sum(item.juego.precio * item.cantidad for item in items)

    return render(request, 'carrito.html', {
        'items': items,
        'total': total
    })


@login_required
@require_POST
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')


@login_required
@transaction.atomic
def confirmar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    items = carrito.items.select_related('juego')

    if not items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')

    total = sum(item.juego.precio * item.cantidad for item in items)
    compra = Compra.objects.create(usuario=request.user, total=total)

    for item in items:
        DetalleCompra.objects.create(
            compra=compra,
            juego=item.juego,
            precio_unitario=item.juego.precio
        )

    carrito.items.all().delete()
    messages.success(request, "Compra realizada con éxito.")
    return redirect('ver_factura', compra_id=compra.id)


@login_required
def ver_factura(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    detalles = DetalleCompra.objects.filter(compra=compra)
    email = request.user.email

    return render(request, 'factura.html', {
        'compra': compra,
        'detalles': detalles,
        'email': email
    })


# -----------------------------
# FUNCIONES PARA ADMINISTRADORES
# -----------------------------

@staff_member_required
def ver_compras(request):
    compras = Compra.objects.select_related('usuario').prefetch_related('detallecompra_set__juego')
    return render(request, 'compras_admin.html', {'compras': compras})


@staff_member_required
def ver_factura_admin(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    detalles = DetalleCompra.objects.filter(compra=compra)
    email = compra.usuario.email

    return render(request, 'factura.html', {
        'compra': compra,
        'detalles': detalles,
        'email': email
    })


@staff_member_required
def administrar_compras(request):
    compras = Compra.objects.select_related('usuario').all()

    if request.method == 'POST':
        compra_id = request.POST.get('compra_id')
        nuevo_estado = request.POST.get('estado')
        compra = get_object_or_404(Compra, id=compra_id)
        compra.estado = nuevo_estado
        compra.save()
        return redirect('administrar_compras')

    return render(request, 'administrar_compras.html', {'compras': compras})

def mas_vendidos(request):
    top_juegos = (DetalleCompra.objects
                  .values('juego')
                  .annotate(total_vendidos=models.Count('id'))
                  .order_by('-total_vendidos')[:10])

    juegos = []
    for posicion, item in enumerate(top_juegos, start=1):
        juego = Juego.objects.get(id=item['juego'])
        juegos.append({
            'posicion': posicion,
            'juego': juego,
            'total_vendidos': item['total_vendidos']
        })

    return render(request, 'mas_vendidos.html', {'juegos': juegos})

