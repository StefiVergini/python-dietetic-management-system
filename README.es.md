**Read this in other languages:** [English](README.md)

> 💡 **Nota**
>
> Esta aplicación crea automáticamente la base de datos, tablas y los registros iniciales durante la primera ejecución del sistema. Hace que el proceso de configuración sea mucho más simple. 

# 🥗 Nutrite - Sistema de Gestión para Dietética (Backend)

## 💼 Sobre este proyecto

Nutrite es una aplicación backend desarrollada en Python como parte de mi proceso de formación como Backend Developer.

El objetivo del proyecto fue diseñar un sistema modular capaz de administrar las operaciones principales de una dietética utilizando Programación Orientada a Objetos y una base de datos relacional.

Durante su desarrollo trabajé principalmente en el diseño de la arquitectura, la organización del código por módulos, la implementación de operaciones CRUD y el modelado de la base de datos.

Aunque el proyecto fue desarrollado como una aplicación de consola, representa una de las bases de mi experiencia en desarrollo backend.

---

# 📌 Descripción

Nutrite es un sistema de gestión modular que permite administrar las principales entidades de una dietética.

La aplicación está organizada por módulos independientes para facilitar su mantenimiento y escalabilidad.

---

# 💡 Contexto del negocio

## Problema

Muchos pequeños comercios administran clientes, proveedores, productos y ventas de forma manual, dificultando el control de la información.

## Solución

Nutrite centraliza toda esa información permitiendo:

- Gestión de clientes
- Gestión de proveedores
- Gestión de artículos
- Gestión de ventas
- Gestión de pedidos
- Validaciones de datos
- Creación automática de la base de datos

---

# ⚙️ Funcionalidades

✔ Gestión de Clientes

- Alta
- Modificación
- Eliminación
- Búsqueda

---

✔ Gestión de Proveedores

- Alta
- Modificación
- Eliminación
- Consulta

---

✔ Gestión de Artículos

- Alta
- Actualización de stock
- Modificación
- Eliminación

---

✔ Gestión de Ventas

- Registro de ventas
- Cálculo de importes
- Administración de productos vendidos

---

✔ Base de Datos

El sistema crea automáticamente:

- Base de datos
- Tablas
- Relaciones
- Datos iniciales

No requiere ejecutar scripts SQL manualmente.

---

# 🏗️ Arquitectura

```
main.py
│
├── submenus.py
│
├── clientes.py
├── proveedores.py
├── articulos.py
├── ventas.py
├── pedidoDevo.py
│
├── validaciones.py
│
└── Bd_Nutrite.py
```

Cada módulo posee una responsabilidad específica, facilitando la organización y escalabilidad del proyecto.

---

# 🧰 Tecnologías

- Python
- MariaDB / MySQL
- SQL
- Programación Orientada a Objetos
- Arquitectura Modular

---

# 🧠 Aprendizajes

Este proyecto me permitió profundizar en:

- Arquitectura Backend
- Desarrollo CRUD
- Modelado de bases de datos
- SQL
- Programación Orientada a Objetos
- Validaciones
- Separación de responsabilidades
- Organización de proyectos Python

Este sistema fue una de las bases que posteriormente me permitió avanzar hacia FastAPI, PostgreSQL, Docker y aplicaciones potenciadas por Inteligencia Artificial.

---


# 📷 Capturas

### Menú Principal

![Menu-Principal](screenshots/main-menu.png)

---

### Gestión de Proveedores

![Proveedores](screenshots/supplier-management.png)

---

### Gestión de Artículos

![Articulos](screenshots/items-management.png)

---

### Gestión de Clientes

![Clientes](screenshots/client-management.png)

---

### Gestión Ventas

![Ventas](screenshots/sales-management.png)

---

### Generación de Factura

![Factura](screenshots/invoice.png)

---

# 🚀 Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/StefiVergini/python-dietetic-management-system.git
cd python-dietetic-management-system
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Configurar MariaDB / MySQL

Crear una instancia local de MariaDB (o MySQL).

Modificar las credenciales de conexión en:

```
Bd_Nutrite.py
```

Ejemplo:

```python
host="localhost"
user="root"
password="tu_contraseña"
```

## 4. Ejecutar el proyecto

```bash
python main.py
```

En la primera ejecución el sistema crea automáticamente:

- Base de datos
- Tablas
- Relaciones
- Datos iniciales

---

# 👩‍💻 Autora

**Stefanía Vergini**

Backend Developer • Data & AI Engineering

GitHub:
https://github.com/StefiVergini

# 📄 Licencia

Este proyecto fue desarrollado con fines educativos y para mi portfolio profesional.