from django.shortcuts import render
from .steam_service import buscar_juegos, obtener_detalle_juego
import requests

def buscar_juegos_view(request):
    query = request.GET.get('query', '')
    juegos = buscar_juegos(query) if query else []
    return render(request, 'resultados_busqueda.html', {
        'query': query,
        'juegos': juegos,
    })

# def detalle_juego_steam_view(request, appid):
#     detalle = obtener_detalle_juego(appid)
#     print("DETALLE COMPLETO:", detalle)  # Ver qué recibes realmente
    
#     contexto = {
#         'juego': {
#             'name': detalle.get('name', 'Nombre no disponible'),
#             'short_description': detalle.get('short_description', ''),
#             'developers': detalle.get('developers', ['Desarrollador desconocido']),
#             'genres': detalle.get('genres', []),
#             'release_date': detalle.get('release_date', {}),
#             'header_image': detalle.get('header_image', ''),
#             'screenshots': detalle.get('screenshots', []),
#         }
#     }

#     return render(request, 'detalle_juego_steam.html', contexto)


def detalle_juego_steam_view(request, appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=spanish"
    response = requests.get(url)
    data = response.json()

    juego_data = data.get(str(appid), {}).get('data', {})

    juego = {
        'nombre': juego_data.get('name'),
        'descripcion_corta': juego_data.get('short_description', ''),
        'descripcion': juego_data.get('detailed_description', ''),
        'desarrollador': ', '.join(juego_data.get('developers', [])),
        'genero': ', '.join([g['description'] for g in juego_data.get('genres', [])]),
        'fecha_lanzamiento': juego_data.get('release_date', {}).get('date'),
        'precio': juego_data.get('price_overview', {}).get('final_formatted', 'Gratis'),

        'video': juego_data.get('movies', [{}])[0].get('webm', {}).get('480', None) if juego_data.get('movies') else None,
        'imagen_principal': juego_data.get('header_image'),
        'screenshots': juego_data.get('screenshots', []),
    }

    return render(request, 'detalle_juego_steam.html', {'juego': juego})