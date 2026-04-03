from django.urls import path
from . import views

urlpatterns = [
    path('',                             views.dashboard,         name='dashboard'),
    path('login/',                       views.login_view,        name='login'),
    path('logout/',                      views.logout_view,       name='logout'),
    path('productos/',                   views.lista_productos,   name='lista_productos'),
    path('productos/crear/',             views.crear_producto,    name='crear_producto'),
    path('productos/editar/<int:pk>/',   views.editar_producto,   name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/exportar/',          views.exportar_excel,    name='exportar_excel'),
    path('usuarios/',                    views.lista_usuarios,    name='lista_usuarios'),
    path('usuarios/crear/',              views.crear_usuario,     name='crear_usuario'),
    path('usuarios/eliminar/<int:pk>/',  views.eliminar_usuario,  name='eliminar_usuario'),
    path('historial/',                   views.historial,         name='historial'),
    path('productos/venta/<int:pk>/',    views.registrar_venta,   name='registrar_venta'),
]