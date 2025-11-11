# 🚀 Evory Drive - Gestión Ágil

## Descripción del Proyecto

Evory Drive es una plataforma web que permiten a los clientes, asignados por compañías asociadas, solicitar servicios de transporte personalizados tanto para traslados puntuales como para servicios de varios días.


---

## ⚙️ Requisitos Previos

Asegúrate de tener instalado:

* **Python 3.x**
* **pip**
* **Node.js y npm**

---

## 🛠️ Guía de Configuración e Inicio

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### 1. Preparación del Entorno

1.  **Crear el entorno virtual:**
    ```bash
    python -m venv env
    ```

2.  **Activar el entorno virtual:**
    * **Windows:**
        ```bash
        env\Scripts\activate
        ```
    * **Linux/macOS:**
        ```bash
        source env/bin/activate
        ```

3.  **Instalar las dependencias de Python (Backend):**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instalar las dependencias del Frontend (Node.js):**
    ```bash
    npm install
    ```

### 2. Configuración Inicial de Django

*(Este paso es solo si el proyecto es nuevo; si ya existe, ignóralo)*
5.  **Inicializar el proyecto Django (si es necesario):**
    ```bash
    django-admin startproject evory_drive .
    ```

6.  **Crear las migraciones** (Estructura de la base de datos):
    ```bash
    python manage.py makemigrations
    ```

7.  **Aplicar las migraciones** a la base de datos:
    ```bash
    python manage.py migrate
    ```

8.  **Crear un Superusuario** para el panel de administración:
    ```bash
    python manage.py createsuperuser
    ```

### 3. Ejecución del Servidor

9.  **Iniciar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

---

## 🗺️ Rutas Principales (Endpoints)

El servidor de desarrollo corre en `http://127.0.0.1:8000/`. 

* **Panel de Administración Django:**
    `http://127.0.0.1:8000/admin/`
