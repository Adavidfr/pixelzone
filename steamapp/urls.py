from django.urls import path
from . import views

urlpatterns = [
    path('buscar_juegos/', views.buscar_juegos_view, name='buscar_juegos'),
    path('juego-steam/<int:appid>/', views.detalle_juego_steam_view, name='detalle_juego_steam'),
]
