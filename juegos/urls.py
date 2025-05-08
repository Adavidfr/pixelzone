from django.urls import path
from . import views

urlpatterns = [
    # path('', views.inicio, name='inicio'),
    path('juegos/', views.lista_juegos, name='lista_juegos'),
    path('agregar/', views.agregar_juego, name='agregar_juego'),
    # path('buscar/', views.buscar_juego, name='detalle_juego_por_id'),
    path('<int:appid>/', views.detalle_juego, name='detalle_juego'),
]
