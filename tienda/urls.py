# tienda/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('carrito/agregar/<int:juego_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/confirmar/', views.confirmar_compra, name='confirmar_compra'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('factura/<int:compra_id>/', views.ver_factura, name='ver_factura'),
    path('compras/', views.ver_compras, name='ver_compras'), 
    path('admin/compras/', views.administrar_compras, name='administrar_compras'),
    path('admin/compras/factura/<int:compra_id>/', views.ver_factura_admin, name='ver_factura_admin'), 
    path('admin/compras/', views.administrar_compras, name='administrar_compras'),
    path('mas-vendidos/', views.mas_vendidos, name='mas_vendidos')
]
