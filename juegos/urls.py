from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Nueva vista de redirección
    path('buscar/', views.buscar_juego, name='detalle_juego_por_id'),
    path('<int:appid>/', views.detalle_juego, name='detalle_juego'),
]
