# 👕 StockApp — Sistema de Control de Inventario

Sistema web de gestión de inventario para negocios de indumentaria. Desarrollado con Django, Tailwind CSS y DaisyUI.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-4.2.20-green)
![MySQL](https://img.shields.io/badge/MySQL-MariaDB_10.4-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## Capturas

### 🔐 Login

<img width="1593" height="766" alt="image" src="https://github.com/user-attachments/assets/a9335407-8c4c-4849-b677-fa876f553a38" />

### 📊 Dashboard

<img width="1577" height="532" alt="image" src="https://github.com/user-attachments/assets/5ca85bef-d803-4330-ac4f-c8a764a29b4d" />

### 📦 Productos

<img width="1571" height="683" alt="image" src="https://github.com/user-attachments/assets/7a6e6692-7338-4c02-9a0a-521c4363c298" />

### 👥 Usuarios

<img width="1447" height="503" alt="image" src="https://github.com/user-attachments/assets/b460417d-938d-43fa-bf64-48661ef8509c" />

### 📋 Historial

<img width="1579" height="739" alt="image" src="https://github.com/user-attachments/assets/b4318607-dfe9-46fe-b42c-ed8ec8b5e8ee" />

---

## Características

- Autenticación — Login/logout con sesión y timeout de inactividad (2 minutos)
- Dashboard — Métricas en tiempo real: stock total, productos, categorías y ventas del día
- CRUD de productos — Crear, editar y eliminar con foto comprimida automáticamente (max 800x800px)
- Registro de ventas — Descuento de stock con confirmación de cantidad y registro en historial
- Alertas de stock bajo — Notificación visual con punto parpadeante cuando hay productos con 5 o menos unidades
- Filtros avanzados — Por nombre, categoría, talle y stock bajo con paginación de a 10
- Exportar a Excel — Con formato, encabezados de color y ancho de columnas automático
- Gestión de usuarios — Roles: Admin y Usuario con permisos diferenciados
- Historial de cambios — Registra quién creó, editó, vendió o eliminó cada producto y cuándo
- Ventas por día — Últimos 5 días con hora local Argentina
- Productos más vendidos — Top 5 histórico calculado desde el historial
- Modo claro/oscuro — Toggle con persistencia en el navegador
- Responsive — Menú hamburguesa en mobile

---

## Roles y permisos

| Rol | Acceso |
| --- | --- |
| Admin | Todo el sistema — productos, usuarios, historial y exportación |
| Usuario | Solo productos — cargar, editar, eliminar y registrar ventas |

---

## Estados de stock

| Color | Rango | Descripción |
| --- | --- | --- |
| 🟢 Verde | +5 unidades | Stock normal |
| 🟡 Amarillo | 1 a 5 unidades | Stock bajo |
| 🔴 Rojo | 0 unidades | Sin stock |

---

## Stack tecnológico

| Tecnología | Uso |
| --- | --- |
| Python 3.12 | Backend |
| Django 4.2.20 | Framework principal |
| MySQL / MariaDB 10.4 | Base de datos |
| Tailwind CSS v4 + DaisyUI | Estilos y componentes UI |
| Node.js LTS | Compilación de Tailwind |
| Pillow | Compresión y manejo de imágenes |
| openpyxl | Exportación a Excel |
| Inter (Google Fonts) | Tipografía |

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/btoledo1992/InventarioControl-Django.git
cd InventarioControl-Django
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install django==4.2.20 mysqlclient django-tailwind pillow openpyxl
```

### 4. Crear la base de datos en MySQL

```sql
CREATE DATABASE stockapp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar la base de datos

Abrí `stockapp/settings.py` y completá con tus datos:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stockapp_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Configurar la ruta de npm (Windows)

En `stockapp/settings.py`:

```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

Para encontrar tu ruta ejecutá:
```bash
Get-Command node
```

### 7. Instalar Tailwind CSS

```bash
python manage.py tailwind install
```

### 8. Aplicar migraciones

```bash
python manage.py migrate
```

### 9. Crear superusuario

```bash
python manage.py createsuperuser
```

### 10. Correr el servidor

Necesitás **dos terminales** abiertas al mismo tiempo:

**Terminal 1 — Tailwind:**
```bash
python manage.py tailwind start
```

**Terminal 2 — Django:**
```bash
python manage.py runserver
```

Entrar a http://127.0.0.1:8000 y loguearse con el superusuario.

---

## URLs disponibles

| URL | Descripción |
| --- | --- |
| / | Dashboard principal |
| /productos/ | Lista de productos con filtros |
| /productos/crear/ | Nuevo producto |
| /productos/exportar/ | Exportar a Excel |
| /usuarios/ | Gestión de usuarios *(solo admin)* |
| /historial/ | Historial de cambios *(solo admin)* |
| /admin/ | Panel Django Admin |

---

## Estructura del proyecto

```
InventarioControl-Django/
│
├── stockapp/
│   ├── settings.py
│   └── urls.py
│
├── inventario/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── lista.html
│   │   ├── formulario.html
│   │   ├── confirmar_eliminar.html
│   │   ├── registrar_venta.html
│   │   ├── historial.html
│   │   └── usuarios/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
│
├── theme/
├── media/
├── .gitignore
├── manage.py
└── README.md
```

---

## Modelos principales

**Categoría**

| Campo | Tipo |
| --- | --- |
| nombre | CharField |

**Producto**

| Campo | Tipo |
| --- | --- |
| nombre | CharField |
| categoria | ForeignKey |
| talle | CharField (XS/S/M/L/XL/XXL) |
| color | CharField |
| precio | DecimalField |
| stock | PositiveIntegerField |
| foto | ImageField |
| creado | DateTimeField |

**Historial**

| Campo | Tipo |
| --- | --- |
| usuario | ForeignKey |
| accion | CharField (crear/editar/eliminar/venta) |
| producto | CharField |
| descripcion | TextField |
| fecha | DateTimeField |

---

## Solución de errores comunes

**MariaDB 10.6 or later is required**

```bash
pip install django==4.2.20
```

**node.js and/or npm is not installed**

Agregá en `settings.py`:
```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

**Las ventas de hoy no aparecen en el dashboard**

Verificar en `settings.py`:
```python
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_TZ = True
```

**El editar no guarda los cambios**

Verificar que el formulario tenga:
```html
<form method="POST" enctype="multipart/form-data">
```

---

## Autor

Desarrollado por **Blas Emanuel Toledo** — [@btoledo](https://github.com/btoledo1992)

Ushuaia, Argentina — desarrollo & infraestructura

https://github.com/btoledo1992

> Proyecto desarrollado como parte del proceso de aprendizaje de desarrollo web fullstack con Django.
