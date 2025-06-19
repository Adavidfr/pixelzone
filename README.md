# PixelZone

PixelZone es una tienda virtual de videojuegos inspirada en Steam, desarrollada con Django. Permite a los usuarios explorar, buscar y comprar juegos, así como a los administradores gestionar el catálogo y las compras. Incluye integración con la API de Steam para búsqueda de juegos y un sistema de carrito de compras.

## Características principales

- **Catálogo de juegos**: Visualiza juegos con imágenes, descripciones, videos y filtros por género.
- **Búsqueda avanzada**: Busca juegos por nombre o género, incluyendo integración con la API de Steam.
- **Carrito de compras**: Añade juegos al carrito y realiza compras.
- **Gestión de usuarios**: Registro, inicio de sesión y roles de usuario (usuario normal y administrador).
- **Administración**: Los administradores pueden agregar, editar y eliminar juegos, así como ver y gestionar compras.
- **Facturación**: Visualización de facturas de compra para usuarios y administradores.

## Instalación

1. **Clona el repositorio**

   ```sh
   git clone https://github.com/Adavidfr/pixelzone.git
   cd pixelzone
   ```

2. **Crea un entorno virtual (opcional pero recomendado)**

   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias necesarias**

   ```sh
   pip install django
   pip install python-steam-api
   pip install django-widget-tweaks
   ```

4. **Realiza las migraciones**

   ```sh
   python manage.py migrate
   ```

5. **Crea un superusuario para acceder al panel de administración**

   ```sh
   python manage.py createsuperuser
   ```

6. **Inicia el servidor de desarrollo**

   ```sh
   python manage.py runserver
   ```

7. **Accede a la aplicación**
   - Sitio principal: [http://localhost:8000/](http://localhost:8000/)
   - Panel de administración: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Estructura del proyecto

- `juegos/`: Gestión del catálogo de juegos.
- `tienda/`: Carrito de compras, compras y facturación.
- `steamapp/`: Integración con la API de Steam.
- `usuarios/`: Registro e inicio de sesión de usuarios.
- `templates/`: Plantillas HTML base y compartidas.

## Dependencias principales

- Django
- python-steam-api
- django-widget-tweaks

## Funcionalidades destacadas

- Registro e inicio de sesión de usuarios.
- Visualización y filtrado de juegos.
- Carrito de compras y proceso de compra.
- Administración de juegos y compras.
- Búsqueda de juegos en Steam.

## Notas

- Asegúrate de tener Python 3.8+ instalado.
- Puedes personalizar la clave de la API de Steam en [`steamapp/steam_service.py`](steamapp/steam_service.py).

---

¡Gracias por usar PixelZone!
