# 👕 StockApp — Sistema de Control de Inventario

Sistema web desarrollado con **Django + MySQL** para la gestión de inventario en negocios de indumentaria. Permite administrar productos, registrar ventas, gestionar usuarios y visualizar métricas en tiempo real mediante un dashboard completo.

---

## 📸 Capturas

### 🔐 Login
![Login]<img width="1593" height="766" alt="image" src="https://github.com/user-attachments/assets/a9335407-8c4c-4849-b677-fa876f553a38" />

### 📊 Dashboard
![Dashboard]<img width="1577" height="532" alt="image" src="https://github.com/user-attachments/assets/5ca85bef-d803-4330-ac4f-c8a764a29b4d" />

### 📦 Productos
![Productos]<img width="1571" height="683" alt="image" src="https://github.com/user-attachments/assets/7a6e6692-7338-4c02-9a0a-521c4363c298" />

### 👥 Usuarios
![Usuarios]<img width="1593" height="474" alt="image" src="https://github.com/user-attachments/assets/54d3a095-3b21-427e-ac33-7d9e7b6b526a" />

### 📋 Historial
![Historial]<img width="1579" height="739" alt="image" src="https://github.com/user-attachments/assets/b4318607-dfe9-46fe-b42c-ed8ec8b5e8ee" />

---

## ✨ Características

- 🔐 **Autenticación** — Login/logout con sesión y timeout de inactividad
- 📊 **Dashboard** — Métricas en tiempo real: stock total, productos, categorías, alertas
- 📦 **CRUD de productos** — Crear, editar, eliminar con foto comprimida automáticamente
- 🛒 **Registro de ventas** — Descuento de stock con historial completo
- 🔔 **Alertas de stock bajo** — Notificación visual con punto parpadeante
- 🔍 **Filtros avanzados** — Por nombre, categoría, talle y stock bajo
- 📄 **Paginación** — De a 10 productos por página
- 📤 **Exportar a Excel** — Con formato y encabezados de color
- 👥 **Gestión de usuarios** — Roles: Admin y Usuario con permisos diferenciados
- 📋 **Historial de cambios** — Registra quién hizo qué y cuándo
- 📈 **Ventas por día** — Últimos 5 días con hora local Argentina
- 🏆 **Productos más vendidos** — Top 5 histórico
- 🌙 **Modo claro/oscuro** — Con memoria en el navegador
- 📱 **Diseño responsive** — Menú hamburguesa en mobile

---

## 🛠️ Stack tecnológico

| Tecnología | Uso |
|---|---|
| Python 3.12 | Backend |
| Django 4.2.20 | Framework principal |
| MySQL / MariaDB 10.4+ | Base de datos |
| Tailwind CSS v4 + DaisyUI | Estilos y componentes UI |
| Node.js LTS | Compilación de Tailwind |
| Pillow | Compresión de imágenes |
| openpyxl | Exportación a Excel |

---

## 🚀 Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/TuUsuario/InventarioControl-Django.git
cd InventarioControl-Django
```

### 2. Crear y activar el entorno virtual

```bash
# Crear
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Mac/Linux)
source .venv/bin/activate
```

### 3. Instalar dependencias Python

```bash
pip install django==4.2.20 mysqlclient django-tailwind pillow openpyxl
```

### 4. Crear la base de datos en MySQL

Abrí tu cliente MySQL (phpMyAdmin, Workbench, etc.) y ejecutá:

```sql
CREATE DATABASE stockapp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar la base de datos

Abrí `stockapp/settings.py` y configurá:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stockapp_db',
        'USER': 'root',         # tu usuario MySQL
        'PASSWORD': '',         # tu contraseña MySQL
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Configurar la ruta de npm (Windows)

En `stockapp/settings.py` verificá que esté esta línea con tu ruta de Node:

```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

Para encontrar tu ruta ejecutá en la terminal:
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

### 10. Correr el proyecto

Necesitás **dos terminales** abiertas al mismo tiempo:

**Terminal 1 — Tailwind:**
```bash
.venv\Scripts\activate
python manage.py tailwind start
```

**Terminal 2 — Django:**
```bash
.venv\Scripts\activate
python manage.py runserver
```

---

## 🌐 URLs disponibles

| URL | Descripción |
|---|---|
| `http://127.0.0.1:8000/` | Dashboard principal |
| `http://127.0.0.1:8000/productos/` | Lista de productos |
| `http://127.0.0.1:8000/usuarios/` | Gestión de usuarios *(solo admin)* |
| `http://127.0.0.1:8000/historial/` | Historial de cambios *(solo admin)* |
| `http://127.0.0.1:8000/admin/` | Panel de administración Django |

---

## 🗂️ Estructura del proyecto

```
InventarioControl-Django/
│
├── inventario/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── lista.html
│   │   ├── formulario.html
│   │   ├── historial.html
│   │   ├── registrar_venta.html
│   │   └── usuarios/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
│
├── stockapp/
│   ├── settings.py
│   └── urls.py
│
├── theme/              ← Tailwind CSS
├── media/              ← Imágenes subidas (no incluido en repo)
├── manage.py
└── README.md
```

---

## 🧠 Modelos principales

### Categoría
| Campo | Tipo |
|---|---|
| nombre | CharField |

### Producto
| Campo | Tipo |
|---|---|
| nombre | CharField |
| categoria | ForeignKey |
| talle | CharField (XS/S/M/L/XL/XXL) |
| color | CharField |
| precio | DecimalField |
| stock | PositiveIntegerField |
| foto | ImageField |
| creado | DateTimeField |

### Historial
| Campo | Tipo |
|---|---|
| usuario | ForeignKey |
| accion | CharField (crear/editar/eliminar/venta) |
| producto | CharField |
| descripcion | TextField |
| fecha | DateTimeField |

---

## ⚠️ Solución de errores comunes

**Error: `MariaDB 10.6 or later is required`**
```bash
pip install django==4.2.20
```

**Error: `node.js and/or npm is not installed`**

Agregá en `settings.py`:
```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

**Las ventas de hoy no aparecen en el dashboard**

Verificá en `settings.py`:
```python
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_TZ = True
```

---

## 📄 Licencia

Proyecto de uso educativo y adaptable a entornos productivos.

---

## 👨‍💻 Autor

Desarrollado por **Blas Emanuel Toledo** — [@btoledo](https://github.com/btoledo1992)

> Proyecto desarrollado como parte del proceso de aprendizaje de desarrollo web fullstack con Django.
