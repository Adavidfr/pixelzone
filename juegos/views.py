from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Juego

def lista_juegos(request):
    juegos = Juego.objects.all()
    return render(request, 'lista_juegos.html', {'juegos': juegos})

def agregar_juego(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        imagen_miniatura = request.POST.get('imagen_miniatura')
        imagen_principal = request.POST.get('imagen_principal')
        imagen2 = request.POST.get('imagen2')
        imagen3 = request.POST.get('imagen3')
        imagen4 = request.POST.get('imagen4')
        imagen5 = request.POST.get('imagen5')
        video = request.POST.get('video')
        descripcion = request.POST.get('descripcion')
        fecha_lanzamiento = request.POST.get('fecha_lanzamiento')
        desarrollador = request.POST.get('desarrollador')
        genero = request.POST.get('genero')
        descuento = request.POST.get('descuento')

        Juego.objects.create(
            nombre=nombre,
            precio=precio,
            imagen_miniatura=imagen_miniatura,
            imagen_principal=imagen_principal,
            imagen2=imagen2,
            imagen3=imagen3,
            imagen4=imagen4,
            imagen5=imagen5,
            video=video,
            descripcion=descripcion,
            fecha_lanzamiento=fecha_lanzamiento,
            desarrollador=desarrollador,
            genero=genero,
            descuento=descuento
        )
        return redirect('lista_juegos')
    return render(request, 'agregar_juego.html')

def detalle_juego(request, appid):
    juego = get_object_or_404(Juego, id=appid)
    imagenes_extra = [juego.imagen2, juego.imagen3, juego.imagen4, juego.imagen5]
    return render(request, 'detalle_juego.html', {
        'juego': juego,
        'imagenes_extra': imagenes_extra,
    })

