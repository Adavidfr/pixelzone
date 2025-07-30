from django.urls import path
from . import views

urlpatterns = [
    path('', views.juegos_populares_view, name='juegos_populares'),
    path('buscar_juegos/', views.buscar_juegos_view, name='buscar_juegos'),
    path('juego/<int:appid>/', views.detalle_juego_api_view, name='detalle_juego_api'),
]
