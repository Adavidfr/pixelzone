import os
from dotenv import load_dotenv
from steam_web_api import Steam
import requests
from decimal import Decimal

load_dotenv()

KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)

def buscar_juegos(query):
    try:
        search_response = steam.apps.search_games(query)
        juegos = search_response.get('apps', [])

        juegos_actualizados = []
        for juego in juegos:
            appid = juego.get('id', [None])[0]
            if not appid:
                continue

            detalle_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=spanish"
            detalle_response = requests.get(detalle_url)
            detalle_data = detalle_response.json().get(str(appid), {}).get('data', {})

            imagen_principal = detalle_data.get('header_image', "/static/img/no_image_available.png")

            # Obtener info de precios
            price_overview = detalle_data.get('price_overview', {})
            precio_original_cents = price_overview.get('initial', 0)
            precio_final_cents = price_overview.get('final', 0)
            descuento = price_overview.get('discount_percent', 0)

            precio_original = Decimal(precio_original_cents) / 100 if precio_original_cents else Decimal(0)
            precio_final = Decimal(precio_final_cents) / 100 if precio_final_cents else Decimal(0)

            juegos_actualizados.append({
                'appid': appid,
                'name': juego.get('name', 'Sin nombre'),
                'img': imagen_principal,
                'final_price': precio_final,
                'original_price': precio_original,
                'discount_percent': descuento,
            })

        return juegos_actualizados

    except Exception as e:
        print("ERROR EN BUSQUEDA:", e)
        return []

def obtener_juegos_populares():
    """
    Obtiene los 30 juegos más jugados actualmente en Steam con detalles de precios y descuentos.
    """
    try:
        url = f"https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/?key={KEY}"
        response = requests.get(url)
        data = response.json()

        juegos_raw = data.get('response', {}).get('ranks', [])[:100]  # Top 30

        juegos = []
        for juego in juegos_raw:
            appid = juego.get('appid')

            # Obtener detalles del juego desde la API de Steam Store
            detalle_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=spanish"
            detalle_response = requests.get(detalle_url)
            detalle_data = detalle_response.json().get(str(appid), {}).get('data', {})

            if detalle_data:
                # Obtener información de precios
                price_overview = detalle_data.get('price_overview', {})
                precio_original_cents = price_overview.get('initial', 0)
                precio_final_cents = price_overview.get('final', 0)
                descuento = price_overview.get('discount_percent', 0)

                precio_original = Decimal(precio_original_cents) / 100 if precio_original_cents else Decimal(0)
                precio_final = Decimal(precio_final_cents) / 100 if precio_final_cents else Decimal(0)

                # Agregar el juego a la lista
                juegos.append({
                    'appid': appid,
                    'name': detalle_data.get('name', 'Sin nombre'),
                    'img': detalle_data.get('header_image', "/static/img/no_image_available.png"),
                    'final_price': precio_final,
                    'original_price': precio_original,
                    'discount_percent': descuento,
                    'categoria': "Más jugado",
                })

        return juegos

    except Exception as e:
        print("ERROR OBTENIENDO JUEGOS MÁS JUGADOS:", e)
        return []