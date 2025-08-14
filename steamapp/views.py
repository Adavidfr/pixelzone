from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .steam_service import buscar_juegos, obtener_juegos_populares
from tienda.models import Carrito, ItemCarrito
from juegos.models import Juego
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
    from django.core.cache import cache
    
    # Check cache first
    cache_key = f"steam_detail_full_{appid}"
    cached_juego = cache.get(cache_key)
    
    if cached_juego:
        return render(request, 'detalle_juego_api.html', {'juego': cached_juego})
    
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
        'appid': appid,
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
    
    # Cache the result for 5 minutes
    cache.set(cache_key, juego, 300)

    return render(request, 'detalle_juego_api.html', {'juego': juego})

@login_required
def agregar_al_carrito_steam_view(request, appid):
    """
    Vista para agregar juegos de Steam al carrito
    """
    from tienda.views import agregar_al_carrito_api
    return agregar_al_carrito_api(request, appid)

def mas_vendidos_api_view(request):
    """
    Vista para mostrar los juegos más vendidos en la API
    """
    from tienda.models import DetalleCompra, DetalleCompraSteam
    from django.db import models
    from django.db.models import Q
    
    # Combinar juegos locales y de Steam
    juegos_combinados = []
    
    # Juegos locales
    juegos_locales = (DetalleCompra.objects
                     .filter(juego__isnull=False)
                     .values('juego__nombre')
                     .annotate(
                         total_vendidos=models.Count('id'),
                         primer_juego_id=models.Min('juego__id')
                     ))
    
    for item in juegos_locales:
        try:
            juego = Juego.objects.get(id=item['primer_juego_id'])
            juegos_combinados.append({
                'nombre': item['juego__nombre'],
                'total_vendidos': item['total_vendidos'],
                'juego': juego,
                'es_steam': False,
                'imagen_url': None
            })
        except Juego.DoesNotExist:
            continue
    
    # Juegos de Steam
    juegos_steam = (DetalleCompraSteam.objects
                   .values('nombre')
                   .annotate(
                       total_vendidos=models.Count('id'),
                       steam_appid=models.Min('steam_appid')
                   ))
    
    for item in juegos_steam:
        juegos_combinados.append({
            'nombre': item['nombre'],
            'total_vendidos': item['total_vendidos'],
            'juego': None,
            'es_steam': True,
            'steam_appid': item['steam_appid'],
            'imagen_url': f"https://cdn.cloudflare.steamstatic.com/steam/apps/{item['steam_appid']}/header.jpg"
        })
    
    # Ordenar por total de ventas y tomar los top 40
    juegos_combinados.sort(key=lambda x: x['total_vendidos'], reverse=True)
    juegos_combinados = juegos_combinados[:40]
    
    # Agregar posiciones
    juegos_finales = []
    for posicion, item in enumerate(juegos_combinados, start=1):
        item['posicion'] = posicion
        juegos_finales.append(item)

    return render(request, 'mas_vendidos_api.html', {
        'juegos': juegos_finales,
        'titulo': 'Más Vendidos',
        'query': ''
    })

def limpiar_cache_steam(request):
    """
    Vista para limpiar el caché de Steam (solo para desarrollo)
    """
    from django.core.cache import cache
    from django.contrib import messages
    
    # Clear all steam-related cache
    cache.clear()
    messages.success(request, "Caché de Steam limpiado exitosamente.")
    
    return redirect('juegos_populares')