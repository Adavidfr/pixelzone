from django.shortcuts import render, redirect

def detalle_juego(request, appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = request.get(url)
    data = response.json()

    if data.get(str(appid)) and data[str(appid)].get("success"):
        juego_data = data[str(appid)]["data"]
        contexto = {
            "nombre": juego_data["name"],
            "descripcion": juego_data.get("short_description", "Sin descripción."),
            "precio": juego_data.get("price_overview", {}),
            "gratis": juego_data.get("is_free", False),
            "imagen": juego_data["header_image"],
            "fecha_lanzamiento": juego_data.get("release_date", {}).get("date", "Fecha no disponible."),
            "desarrollador": juego_data.get("developers", ["Desarrollador desconocido"])[0],
            "genero": juego_data.get("genres", [{"description": "Género desconocido"}])[0]["description"],
            "descuento": juego_data.get("price_overview", {}).get("discount_percent", 0),
            "es_gratis": juego_data.get("is_free", False),
        }
        return render(request, "detalle_juego.html", contexto)
    else:
        return render(request, "error.html", {"mensaje": "Juego no encontrado."})
    
def inicio(request):
        return render(request, 'detalle_juego.html')

def buscar_juego(request):
    appid = request.GET.get('appid')
    if appid:
        return redirect(f'/{appid}/')  # Redirige a la vista detalle_juego
    return redirect('/')  # Si no se ingresa nada, regresa al inicio