from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.dashboard,          name='dashboard'),
    path('productos/',              views.lista_productos,     name='lista_productos'),
    path('productos/crear/',        views.crear_producto,      name='crear_producto'),
    path('productos/editar/<int:pk>/',   views.editar_producto,    name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto,  name='eliminar_producto'),
]