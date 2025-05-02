from django.urls import path
from . import views

urlpatterns = [
    path("juego/<int:appid>/", views.detalle_juego, name="detalle_juego"),
    
    ]