from django.shortcuts import render
from .steam_service import buscar_juegos

def buscar_juegos_view(request):
    query = request.GET.get('query', '')
    juegos = []

    if query:
        juegos = buscar_juegos(query)

    return render(request, 'resultados_busqueda.html', {
        'query': query,
        'juegos': juegos,
    })

