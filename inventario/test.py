from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from inventario.models import Categoria, Producto, Historial


# ================================================================
# HELPERS
# ================================================================

def crear_admin():
    return User.objects.create_superuser(
        username='admin_test',
        password='admin1234',
        email='admin@test.com'
    )

def crear_usuario():
    return User.objects.create_user(
        username='usuario_test',
        password='user1234',
        email='user@test.com'
    )

def crear_categoria():
    return Categoria.objects.create(nombre='Remeras')

def crear_producto(categoria):
    return Producto.objects.create(
        nombre='Remera básica',
        categoria=categoria,
        talle='M',
        color='Blanco',
        precio=Decimal('1500.00'),
        stock=10
    )


# ================================================================
# TESTS DE MODELOS
# ================================================================

class CategoriaModelTest(TestCase):

    def test_crear_categoria(self):
        cat = Categoria.objects.create(nombre='Pantalones')
        self.assertEqual(cat.nombre, 'Pantalones')
        self.assertEqual(str(cat), 'Pantalones')
        print('✅ Categoria: crear y __str__')

    def test_categoria_verbose(self):
        self.assertEqual(Categoria._meta.verbose_name, 'Categoría')
        print('✅ Categoria: verbose_name correcto')


class ProductoModelTest(TestCase):

    def setUp(self):
        self.categoria = crear_categoria()

    def test_crear_producto(self):
        p = crear_producto(self.categoria)
        self.assertEqual(p.nombre, 'Remera básica')
        self.assertEqual(p.stock, 10)
        self.assertEqual(p.precio, Decimal('1500.00'))
        print('✅ Producto: crear con todos los campos')

    def test_str_producto(self):
        p = crear_producto(self.categoria)
        self.assertIn('Remera básica', str(p))
        self.assertIn('M', str(p))
        self.assertIn('Blanco', str(p))
        print('✅ Producto: __str__ correcto')

    def test_stock_default(self):
        p = Producto.objects.create(
            nombre='Test',
            categoria=self.categoria,
            talle='S',
            color='Negro',
            precio=Decimal('1000.00'),
        )
        self.assertEqual(p.stock, 0)
        print('✅ Producto: stock default es 0')

    def test_foto_opcional(self):
        p = crear_producto(self.categoria)
        self.assertFalse(p.foto)
        print('✅ Producto: foto es opcional')

    def test_talles_choices(self):
        talles = [t[0] for t in Producto.TALLES]
        self.assertIn('XS', talles)
        self.assertIn('S', talles)
        self.assertIn('M', talles)
        self.assertIn('L', talles)
        self.assertIn('XL', talles)
        self.assertIn('XXL', talles)
        print('✅ Producto: talles choices correctos')


class HistorialModelTest(TestCase):

    def setUp(self):
        self.user = crear_admin()
        self.categoria = crear_categoria()
        self.producto = crear_producto(self.categoria)

    def test_crear_historial(self):
        h = Historial.objects.create(
            usuario=self.user,
            accion='crear',
            producto='Remera básica',
            descripcion='Talle: M | Color: Blanco | Stock: 10'
        )
        self.assertEqual(h.accion, 'crear')
        self.assertEqual(h.producto, 'Remera básica')
        print('✅ Historial: crear registro')

    def test_acciones_validas(self):
        acciones = [a[0] for a in Historial.ACCIONES]
        self.assertIn('crear', acciones)
        self.assertIn('editar', acciones)
        self.assertIn('eliminar', acciones)
        self.assertIn('venta', acciones)
        print('✅ Historial: acciones válidas correctas')

    def test_ordering_por_fecha(self):
        Historial.objects.create(usuario=self.user, accion='crear', producto='A', descripcion='')
        Historial.objects.create(usuario=self.user, accion='editar', producto='B', descripcion='')
        registros = Historial.objects.all()
        self.assertEqual(registros[0].producto, 'B')
        print('✅ Historial: ordering por fecha desc correcto')


# ================================================================
# TESTS DE AUTENTICACIÓN
# ================================================================

class AuthTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = crear_admin()

    def test_login_correcto(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'admin1234'
        })
        self.assertRedirects(response, reverse('dashboard'))
        print('✅ Auth: login correcto redirige al dashboard')

    def test_login_incorrecto(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        print('✅ Auth: login incorrecto no redirige')

    def test_logout(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        print('✅ Auth: logout redirige al login')

    def test_login_ya_autenticado_redirige(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('dashboard'))
        print('✅ Auth: usuario ya logueado redirige al dashboard')


# ================================================================
# TESTS DE PERMISOS
# ================================================================

class PermisosTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = crear_admin()
        self.usuario = crear_usuario()

    def test_sin_login_redirige_al_login(self):
        urls = ['dashboard', 'lista_productos', 'crear_producto']
        for url in urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response['Location'])
        print('✅ Permisos: sin login redirige al login')

    def test_usuario_no_staff_no_ve_usuarios(self):
        self.client.login(username='usuario_test', password='user1234')
        response = self.client.get(reverse('lista_usuarios'))
        self.assertRedirects(response, reverse('dashboard'))
        print('✅ Permisos: usuario normal no accede a usuarios')

    def test_usuario_no_staff_no_ve_historial(self):
        self.client.login(username='usuario_test', password='user1234')
        response = self.client.get(reverse('historial'))
        self.assertRedirects(response, reverse('dashboard'))
        print('✅ Permisos: usuario normal no accede al historial')

    def test_admin_ve_usuarios(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.get(reverse('lista_usuarios'))
        self.assertEqual(response.status_code, 200)
        print('✅ Permisos: admin accede a usuarios')

    def test_admin_ve_historial(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.get(reverse('historial'))
        self.assertEqual(response.status_code, 200)
        print('✅ Permisos: admin accede al historial')


# ================================================================
# TESTS DE VISTAS
# ================================================================

class DashboardTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = crear_admin()
        self.client.login(username='admin_test', password='admin1234')

    def test_dashboard_carga(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        print('✅ Dashboard: carga correctamente')

    def test_dashboard_contexto(self):
        response = self.client.get(reverse('dashboard'))
        self.assertIn('total_productos', response.context)
        self.assertIn('stock_total', response.context)
        self.assertIn('stock_bajo', response.context)
        self.assertIn('total_categorias', response.context)
        self.assertIn('ultimos', response.context)
        self.assertIn('alertas', response.context)
        print('✅ Dashboard: contexto correcto')


class ProductoVistaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = crear_admin()
        self.categoria = crear_categoria()
        self.producto = crear_producto(self.categoria)
        self.client.login(username='admin_test', password='admin1234')

    def test_lista_productos_carga(self):
        response = self.client.get(reverse('lista_productos'))
        self.assertEqual(response.status_code, 200)
        print('✅ Productos: lista carga correctamente')

    def test_lista_productos_muestra_producto(self):
        response = self.client.get(reverse('lista_productos'))
        self.assertContains(response, 'Remera básica')
        print('✅ Productos: lista muestra el producto')

    def test_crear_producto_get(self):
        response = self.client.get(reverse('crear_producto'))
        self.assertEqual(response.status_code, 200)
        print('✅ Productos: formulario crear carga correctamente')

    def test_crear_producto_post(self):
        response = self.client.post(reverse('crear_producto'), {
            'nombre': 'Jean azul',
            'categoria': self.categoria.id,
            'talle': 'L',
            'color': 'Azul',
            'precio': '2500.00',
            'stock': '5',
        })
        self.assertEqual(Producto.objects.filter(nombre='Jean azul').count(), 1)
        print('✅ Productos: crear producto guarda en la base de datos')

    def test_crear_producto_registra_historial(self):
        self.client.post(reverse('crear_producto'), {
            'nombre': 'Buzo negro',
            'categoria': self.categoria.id,
            'talle': 'XL',
            'color': 'Negro',
            'precio': '3000.00',
            'stock': '8',
        })
        self.assertTrue(Historial.objects.filter(producto='Buzo negro', accion='crear').exists())
        print('✅ Productos: crear registra en historial')

    def test_editar_producto_get(self):
        response = self.client.get(reverse('editar_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 200)
        print('✅ Productos: formulario editar carga correctamente')

    def test_editar_producto_post(self):
        self.client.post(reverse('editar_producto', args=[self.producto.id]), {
            'nombre': 'Remera editada',
            'categoria': self.categoria.id,
            'talle': 'L',
            'color': 'Rojo',
            'precio': '2000.00',
            'stock': '15',
        })
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Remera editada')
        print('✅ Productos: editar actualiza el producto')

    def test_editar_producto_registra_historial(self):
        self.client.post(reverse('editar_producto', args=[self.producto.id]), {
            'nombre': 'Remera editada',
            'categoria': self.categoria.id,
            'talle': 'L',
            'color': 'Rojo',
            'precio': '2000.00',
            'stock': '15',
        })
        self.assertTrue(Historial.objects.filter(accion='editar').exists())
        print('✅ Productos: editar registra en historial')

    def test_eliminar_producto_get(self):
        response = self.client.get(reverse('eliminar_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 200)
        print('✅ Productos: confirmación eliminar carga correctamente')

    def test_eliminar_producto_post(self):
        self.client.post(reverse('eliminar_producto', args=[self.producto.id]))
        self.assertEqual(Producto.objects.filter(id=self.producto.id).count(), 0)
        print('✅ Productos: eliminar borra el producto')

    def test_eliminar_producto_registra_historial(self):
        self.client.post(reverse('eliminar_producto', args=[self.producto.id]))
        self.assertTrue(Historial.objects.filter(accion='eliminar').exists())
        print('✅ Productos: eliminar registra en historial')


# ================================================================
# TESTS DE FILTROS Y PAGINACIÓN
# ================================================================

class FiltrosTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = crear_admin()
        self.categoria = crear_categoria()
        self.client.login(username='admin_test', password='admin1234')

        # Crear 15 productos para probar paginación
        for i in range(15):
            Producto.objects.create(
                nombre=f'Producto {i}',
                categoria=self.categoria,
                talle='M',
                color='Blanco',
                precio=Decimal('1000.00'),
                stock=i
            )

    def test_filtro_por_nombre(self):
        response = self.client.get(reverse('lista_productos') + '?q=Producto 1')
        self.assertEqual(response.status_code, 200)
        print('✅ Filtros: búsqueda por nombre funciona')

    def test_filtro_por_categoria(self):
        response = self.client.get(reverse('lista_productos') + f'?categoria={self.categoria.id}')
        self.assertEqual(response.status_code, 200)
        print('✅ Filtros: filtro por categoría funciona')

    def test_filtro_stock_bajo(self):
        response = self.client.get(reverse('lista_productos') + '?stock_bajo=1')
        self.assertEqual(response.status_code, 200)
        print('✅ Filtros: filtro stock bajo funciona')

    def test_paginacion_primera_pagina(self):
        response = self.client.get(reverse('lista_productos'))
        self.assertEqual(response.status_code, 200)
        print('✅ Paginación: primera página carga correctamente')

    def test_paginacion_segunda_pagina(self):
        response = self.client.get(reverse('lista_productos') + '?page=2')
        self.assertEqual(response.status_code, 200)
        print('✅ Paginación: segunda página carga correctamente')


# ================================================================
# TESTS DE VENTAS
# ================================================================

class VentasTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = crear_admin()
        self.categoria = crear_categoria()
        self.producto = crear_producto(self.categoria)
        self.client.login(username='admin_test', password='admin1234')

    def test_vista_registrar_venta_get(self):
        response = self.client.get(reverse('registrar_venta', args=[self.producto.id]))
        self.assertEqual(response.status_code, 200)
        print('✅ Ventas: formulario venta carga correctamente')

    def test_registrar_venta_descuenta_stock(self):
        self.client.post(reverse('registrar_venta', args=[self.producto.id]), {
            'cantidad': '3'
        })
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 7)
        print('✅ Ventas: registrar venta descuenta stock correctamente')

    def test_registrar_venta_registra_historial(self):
        self.client.post(reverse('registrar_venta', args=[self.producto.id]), {
            'cantidad': '2'
        })
        self.assertTrue(Historial.objects.filter(accion='venta').exists())
        print('✅ Ventas: registrar venta guarda en historial')

    def test_venta_cantidad_mayor_al_stock(self):
        response = self.client.post(reverse('registrar_venta', args=[self.producto.id]), {
            'cantidad': '999'
        })
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)
        print('✅ Ventas: cantidad mayor al stock no modifica el stock')

    def test_venta_cantidad_cero(self):
        self.client.post(reverse('registrar_venta', args=[self.producto.id]), {
            'cantidad': '0'
        })
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)
        print('✅ Ventas: cantidad 0 no modifica el stock')


# ================================================================
# TESTS DE USUARIOS
# ================================================================

class UsuariosTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = crear_admin()
        self.client.login(username='admin_test', password='admin1234')

    def test_lista_usuarios_carga(self):
        response = self.client.get(reverse('lista_usuarios'))
        self.assertEqual(response.status_code, 200)
        print('✅ Usuarios: lista carga correctamente')

    def test_crear_usuario_get(self):
        response = self.client.get(reverse('crear_usuario'))
        self.assertEqual(response.status_code, 200)
        print('✅ Usuarios: formulario crear carga correctamente')

    def test_crear_usuario_post(self):
        self.client.post(reverse('crear_usuario'), {
            'username': 'nuevo_user',
            'email': 'nuevo@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'is_staff': False,
        })
        self.assertTrue(User.objects.filter(username='nuevo_user').exists())
        print('✅ Usuarios: crear usuario guarda en la base de datos')

    def test_eliminar_usuario_post(self):
        usuario = crear_usuario()
        self.client.post(reverse('eliminar_usuario', args=[usuario.id]))
        self.assertFalse(User.objects.filter(id=usuario.id).exists())
        print('✅ Usuarios: eliminar usuario borra correctamente')

    def test_no_puede_eliminarse_a_si_mismo(self):
        response = self.client.post(reverse('eliminar_usuario', args=[self.admin.id]))
        self.assertTrue(User.objects.filter(id=self.admin.id).exists())
        print('✅ Usuarios: admin no puede eliminarse a sí mismo')


# ================================================================
# TESTS DE EXCEL
# ================================================================

class ExcelTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = crear_admin()
        self.categoria = crear_categoria()
        crear_producto(self.categoria)
        self.client.login(username='admin_test', password='admin1234')

    def test_exportar_excel_responde(self):
        response = self.client.get(reverse('exportar_excel'))
        self.assertEqual(response.status_code, 200)
        print('✅ Excel: exportar responde correctamente')

    def test_exportar_excel_content_type(self):
        response = self.client.get(reverse('exportar_excel'))
        self.assertIn('spreadsheetml', response['Content-Type'])
        print('✅ Excel: content-type es xlsx correcto')

    def test_exportar_excel_tiene_attachment(self):
        response = self.client.get(reverse('exportar_excel'))
        self.assertIn('attachment', response['Content-Disposition'])
        print('✅ Excel: response tiene header attachment')