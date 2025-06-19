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
            juego['img'] = juego.get('img', "/static/img/no_image_available.png")

        return juegos

    except Exception as e:
        print("ERROR EN BUSQUEDA:", e)
        return []
