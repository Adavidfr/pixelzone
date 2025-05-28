from django import forms
from .models import Juego

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = [
            'nombre', 
            'precio', 
            'imagen_miniatura', 
            'imagen_principal', 
            'imagen2', 
            'imagen3', 
            'imagen4', 
            'imagen5', 
            'video', 
            'descripcion', 
            'fecha_lanzamiento', 
            'desarrollador', 
            'genero', 
            'descuento'
        ]