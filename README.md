# 🧾 StockApp — Sistema de Control de Inventario

Aplicación web desarrollada con **Django + MySQL** para la gestión de inventario en una empresa de indumentaria. Permite administrar productos, categorías, stock y visualizar información clave mediante un dashboard completo.

---

## 🚀 Características principales

* 📦 Gestión completa de productos (crear, editar, eliminar)
* 🏷️ Organización por categorías
* 📊 Dashboard con métricas en tiempo real:

  * Total de productos
  * Productos con bajo stock
  * Últimos productos agregados
* 🔎 Búsqueda de productos
* 🖼️ Carga de imágenes por producto
* 🔐 Sistema de autenticación (login / logout)
* 📈 Visualización de datos en dashboard (gráficos)
* 📤 Exportación de productos
* 📱 Interfaz responsive (adaptada a dispositivos móviles)
* 🛠️ Panel administrativo integrado (Django Admin)
* 🎨 UI moderna con **Tailwind CSS + DaisyUI**

---

## 🧰 Stack Tecnológico

| Tecnología      | Uso                 |
| --------------- | ------------------- |
| Python 3.12     | Backend             |
| Django 4.2.20   | Framework principal |
| MySQL / MariaDB | Base de datos       |
| Tailwind CSS v4 | Estilos             |
| DaisyUI         | Componentes UI      |
| Node.js         | Entorno frontend    |
| Pillow          | Manejo de imágenes  |

---

## 📌 Descripción del Proyecto

StockApp es un sistema orientado al control de inventario en entornos comerciales, especialmente adaptado para negocios de indumentaria donde se manejan variables como talle, color y categorías de productos.

El sistema permite centralizar la gestión de stock, optimizar el seguimiento de productos y facilitar la toma de decisiones mediante métricas visuales en el dashboard.

---

## 🗂️ Estructura del Proyecto

```
stockapp/
│
├── inventario/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── urls.py
│   └── templates/
│
├── stockapp/
│   ├── settings.py
│   └── urls.py
│
├── media/
└── manage.py
```

---

## 🧠 Modelos principales

### Categoría

* Nombre

### Producto

* Nombre
* Categoría
* Talle (XS - XXL)
* Color
* Precio
* Stock
* Imagen
* Fecha de creación

---

## 📊 Funcionalidades implementadas

* ✔️ CRUD completo de productos
* ✔️ Gestión de categorías
* ✔️ Dashboard con indicadores clave
* ✔️ Detección de stock bajo
* ✔️ Búsqueda dinámica de productos
* ✔️ Sistema de autenticación de usuarios
* ✔️ Panel administrativo con filtros y búsqueda
* ✔️ Visualización de datos mediante gráficos
* ✔️ Exportación de información
* ✔️ Interfaz responsive

---

## 🌐 Accesos del sistema

* Dashboard principal
* Panel de administración
* Gestión de productos

---

## ⚠️ Consideraciones técnicas

* El sistema utiliza **MySQL/MariaDB** como motor de base de datos
* Manejo de archivos multimedia mediante carpeta `media/`
* Integración de Tailwind mediante entorno Node.js
* Arquitectura basada en apps de Django (modular)

---

## 📄 Licencia

Proyecto de uso educativo y adaptable a entornos productivos.

---

## 👨‍💻 Autor

Desarrollado por **[BlasEmanuelToledo / btoledo1992]**


