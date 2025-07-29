from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', views.lista_juegos, name='lista_juegos'),
    path('agregar/', views.agregar_juego, name='agregar_juego'),
    path('<int:id>/', views.detalle_juego, name='detalle_juego'),
    path('editar/<int:id>/', views.editar_juego, name='editar_juego'),
    path('eliminar/<int:id>/', views.eliminar_juego, name='eliminar_juego'),
]
