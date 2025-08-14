from django.urls import path
from . import views

urlpatterns = [
    path('', views.juegos_populares_view, name='juegos_populares'),
    path('lista_juegos_api/', views.juegos_populares_view, name='lista_juegos_api'),
    path('buscar_juegos/', views.buscar_juegos_view, name='buscar_juegos'),
    path('mas-vendidos/', views.mas_vendidos_api_view, name='mas_vendidos_api'),
    path('juego/<int:appid>/', views.detalle_juego_api_view, name='detalle_juego_api'),
    path('juego/<int:appid>/agregar/', views.agregar_al_carrito_steam_view, name='agregar_al_carrito_steam'),
    path('limpiar-cache/', views.limpiar_cache_steam, name='limpiar_cache_steam'),
]
