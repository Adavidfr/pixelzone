from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Juego
from .forms import JuegoForm
from django.db.models import Q, Case, When, IntegerField

def lista_juegos(request):
    consulta = request.GET.get('q', '')
    genero = request.GET.get('genero', '')

    juegos = Juego.objects.all()

    if consulta:
        juegos = juegos.annotate(
            prioridad=Case(
                When(nombre__istartswith=consulta, then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).filter(nombre__icontains=consulta).order_by('prioridad', 'nombre')

    if genero:
        juegos = juegos.filter(genero=genero)

    return render(request, 'lista_juegos.html', {
        'juegos': juegos,
        'mostrar_boton_agregar': request.user.is_superuser,
        'consulta': consulta,
        'genero': genero,
        'form': JuegoForm(),  # 👈 para usar los choices de género en el template
    })

def solo_admin(user):
    return user.is_superuser

@user_passes_test(solo_admin, login_url='/usuarios/login/')
def agregar_juego(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_juegos')
    else:
        form = JuegoForm()
    return render(request, 'agregar_juego.html', {
        'form': form,
    })

def detalle_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    imagenes_extra = [juego.imagen2, juego.imagen3, juego.imagen4, juego.imagen5]
    return render(request, 'detalle_juego.html', {
        'juego': juego,
        'imagenes_extra': imagenes_extra,
    })

@user_passes_test(solo_admin, login_url='/usuarios/login/')
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

@user_passes_test(solo_admin, login_url='/usuarios/login/')
def eliminar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    if request.method == 'POST':
        juego.delete()
        return redirect('lista_juegos')
    return render(request, 'confirmar_eliminacion.html', {'juego': juego})
