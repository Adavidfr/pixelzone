import os
from dotenv import load_dotenv
from steam_web_api import Steam
import requests
from decimal import Decimal
import time
from django.core.cache import cache
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)

# Cache settings
CACHE_TIMEOUT = 300  # 5 minutes
CACHE_PREFIX = "steam_api_"

def hacer_request_con_retry(url, max_retries=3, delay=1):
    """
    Hace una petición HTTP con reintentos en caso de fallo
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} falló para {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                print(f"Todos los intentos fallaron para {url}")
                return None
    return None

def obtener_detalle_juego_paralelo(appid):
    """
    Obtiene detalles de un juego específico
    """
    cache_key = f"{CACHE_PREFIX}detail_{appid}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    detalle_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=spanish"
    detalle_data = hacer_request_con_retry(detalle_url)
    
    if not detalle_data:
        return None
        
    detalle_data = detalle_data.get(str(appid), {}).get('data', {})
    
    if not detalle_data:
        return None

    # Obtener información de precios
    price_overview = detalle_data.get('price_overview', {})
    precio_original_cents = price_overview.get('initial', 0)
    precio_final_cents = price_overview.get('final', 0)
    descuento = price_overview.get('discount_percent', 0)

    precio_original = Decimal(precio_original_cents) / 100 if precio_original_cents else Decimal(0)
    precio_final = Decimal(precio_final_cents) / 100 if precio_final_cents else Decimal(0)

    juego_data = {
        'appid': appid,
        'name': detalle_data.get('name', 'Sin nombre'),
        'img': detalle_data.get('header_image', "/static/img/no_image_available.png"),
        'final_price': precio_final,
        'original_price': precio_original,
        'discount_percent': descuento,
    }
    
    # Cache the result
    cache.set(cache_key, juego_data, CACHE_TIMEOUT)
    return juego_data

def buscar_juegos(query):
    try:
        # Check cache first
        cache_key = f"{CACHE_PREFIX}search_{query}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        search_response = steam.apps.search_games(query)
        juegos = search_response.get('apps', []) if search_response else []

        # Limit to first 20 results for better performance
        juegos = juegos[:20]
        
        # Extract appids
        appids = []
        for juego in juegos:
            appid = juego.get('id', [None])[0]
            if appid:
                appids.append(appid)

        # Get details in parallel
        juegos_actualizados = obtener_detalles_paralelo(appids)
        
        # Cache the result
        cache.set(cache_key, juegos_actualizados, CACHE_TIMEOUT)
        
        return juegos_actualizados

    except Exception as e:
        print("ERROR EN BUSQUEDA:", e)
        return []

def obtener_detalles_paralelo(appids, max_workers=10):
    """
    Obtiene detalles de múltiples juegos en paralelo
    """
    juegos_actualizados = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_appid = {executor.submit(obtener_detalle_juego_paralelo, appid): appid for appid in appids}
        
        # Collect results as they complete
        for future in as_completed(future_to_appid):
            appid = future_to_appid[future]
            try:
                juego_data = future.result()
                if juego_data:
                    juegos_actualizados.append(juego_data)
            except Exception as e:
                print(f"Error obteniendo detalles para appid {appid}: {e}")
    
    return juegos_actualizados

def obtener_juegos_populares():
    """
    Obtiene los juegos más jugados actualmente en Steam con detalles de precios y descuentos.
    """
    try:
        # Check cache first
        cache_key = f"{CACHE_PREFIX}popular"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        url = f"https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/?key={KEY}"
        data = hacer_request_con_retry(url)
        
        if not data:
            print("No se pudo obtener datos de juegos populares")
            return []

        juegos_raw = data.get('response', {}).get('ranks', [])[:50]  # Reduced to 50 for better performance

        # Extract appids
        appids = [juego.get('appid') for juego in juegos_raw if juego.get('appid')]

        # Get details in parallel
        juegos = obtener_detalles_paralelo(appids)
        
        # Add category information
        for juego in juegos:
            juego['categoria'] = "Más jugado"
        
        # Cache the result
        cache.set(cache_key, juegos, CACHE_TIMEOUT)
        
        return juegos

    except Exception as e:
        print("ERROR OBTENIENDO JUEGOS MÁS JUGADOS:", e)
        return []
    

def obtener_detalle_juego_steam(appid):
    return obtener_detalle_juego_paralelo(appid)