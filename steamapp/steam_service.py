from steam_web_api import Steam

KEY = "E45C9A29D547412B6E7FD726562081CF"

steam = Steam(KEY)

def buscar_juegos(query):
    try:
        search_response = steam.apps.search_games(query)
        juegos = search_response.get('apps', [])

        for juego in juegos:
            # Usa directamente la imagen de la API si está disponible
            juego['img'] = juego.get('img', "/static/img/no_image_available.png")

        return juegos

    except Exception as e:
        print("ERROR EN BUSQUEDA:", e)
        return []