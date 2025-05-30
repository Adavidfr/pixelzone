from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Juego
from .forms import JuegoForm

def lista_juegos(request):
    juegos = Juego.objects.all()
    return render(request, 'lista_juegos.html', {
        'juegos': juegos,
        'mostrar_boton_agregar': True
    })


def agregar_juego(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_juegos')
    return render(request, 'agregar_juego.html', {
        'form': JuegoForm(),
    })
               
def detalle_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    imagenes_extra = [juego.imagen2, juego.imagen3, juego.imagen4, juego.imagen5]
    return render(request, 'detalle_juego.html', {
        'juego': juego,
        'imagenes_extra': imagenes_extra,
    })

def editar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES, instance=juego)
        if form.is_valid():
            form.save()
            return redirect('detalle_juego', id=juego.id)
    else:
        form = JuegoForm(instance=juego)
    return render(request, 'editar_juego.html', {
        'form': form,
        'juego': juego,
    })

def eliminar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    
    if request.method == 'POST':
        juego.delete()
        return redirect('lista_juegos')

    return render(request, 'confirmar_eliminacion.html', {'juego': juego})
