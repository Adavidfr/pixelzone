"""
URL configuration for pixelzone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
path('', lambda request: redirect('/usuarios/login/')),
    path('admin/', admin.site.urls),

    # Apps principales
    path('usuarios/', include('usuarios.urls')),
    path('juegos/', include('juegos.urls')),
    path('steam/', include('steamapp.urls')),
    path('tienda/', include('tienda.urls')),

    # Rutas adicionales / redirecciones
    path('steam_buscar/', lambda request: redirect('buscar_juegos')),  # Redirige a la vista de buscar
    
    # Evitar rutas duplicadas o superpuestas
    # path('', include('juegos.urls')),  # <- Comentada porque ya tienes '' redirigiendo a login
]
