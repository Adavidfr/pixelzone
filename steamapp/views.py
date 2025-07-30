from django.shortcuts import render
from .steam_service import buscar_juegos, obtener_juegos_populares
import requests
from decimal import Decimal

def buscar_juegos_view(request):
    query = request.GET.get('query', '')
    juegos = buscar_juegos(query) if query else []
    return render(request, 'resultados_busqueda.html', {
        'query': query,
        'juegos': juegos,
    })

def juegos_populares_view(request):
    """
    Vista para mostrar los juegos más populares de Steam
    """
    query = request.GET.get('query', '')
    
    if query:
        # Si hay búsqueda, usar la función de búsqueda existente
        juegos = buscar_juegos(query)
        titulo = f"Resultados para '{query}'"
    else:
        # Si no hay búsqueda, mostrar juegos populares
        juegos = obtener_juegos_populares()
        titulo = "Tienda"
    
    return render(request, 'lista_juegos_api.html', {
        'juegos': juegos,
        'titulo': titulo,
        'query': query,
    })

def detalle_juego_api_view(request, appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=spanish"
    response = requests.get(url)
    data = response.json()

    juego_data = data.get(str(appid), {}).get('data', {})

    price_overview = juego_data.get('price_overview', {})

    precio_original_cents = price_overview.get('initial', 0)  # Precio original (sin descuento)
    precio_final_cents = price_overview.get('final', 0)      # Precio con descuento

    descuento = price_overview.get('discount_percent', 0)

    precio_original = Decimal(precio_original_cents) / 100 if precio_original_cents else Decimal(0)
    precio_final = Decimal(precio_final_cents) / 100 if precio_final_cents else Decimal(0)

    juego = {
        'nombre': juego_data.get('name'),
        'descripcion_corta': juego_data.get('short_description', ''),
        'descripcion': juego_data.get('detailed_description', ''),
        'desarrollador': ', '.join(juego_data.get('developers', [])),
        'genero': ', '.join([g['description'] for g in juego_data.get('genres', [])]),
        'fecha_lanzamiento': juego_data.get('release_date', {}).get('date'),
        'precio': f"${precio_original:.2f}",
        'precio_con_descuento': f"${precio_final:.2f}",
        'video': juego_data.get('movies', [{}])[0].get('webm', {}).get('480', None) if juego_data.get('movies') else None,
        'imagen_principal': juego_data.get('header_image'),
        'screenshots': juego_data.get('screenshots', []),
        'descuento': descuento,
    }

    return render(request, 'detalle_juego_api.html', {'juego': juego})