import os
from dotenv import load_dotenv
from steam_web_api import Steam

load_dotenv()

KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)

def buscar_juegos(query):
    try:
        search_response = steam.apps.search_games(query)
        juegos = search_response.get('apps', [])

        for juego in juegos:
            # Extraer appid como entero
            juego['appid'] = juego.get('id', [None])[0]
            juego['img'] = juego.get('img', "/static/img/no_image_available.png")

        # Filtrar los juegos que tengan appid
        juegos = [j for j in juegos if j.get('appid')]

        return juegos

    except Exception as e:
        print("ERROR EN BUSQUEDA:", e)
        return []


    
# def obtener_detalle_juego(appid):
#     try:
#         # Forzar cc=us para que venga el precio
#         detalle = steam.apps.get_app_details(appid, cc='us')
#         return detalle.get(str(appid), {}).get('data', {})
#     except Exception as e:
#         print("ERROR EN DETALLE:", e)
#         return {}

def obtener_detalle_juego(appid):
    try:
        detalle = steam.apps.get_app_details(appid)
        print("DETALLE CRUDO:", detalle)
        app_data = detalle.get(str(appid), {})
        if not app_data.get('success'):
            print(f"API dice que no hay éxito para appid {appid}")
            return {}
        return app_data.get('data', {})
    except Exception as e:
        print("ERROR EN DETALLE:", e)
        return {}