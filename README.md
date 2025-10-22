# Evory-drive-gestion-agil

# 1. Crear el entorno virtual
python -m venv env

# 2. Activar el entorno virtual (Windows)
env\Scripts\activate

# 3. Instalar los paquetes necesarios
pip install -r requirements.txt

# 4. Instalar dependencias del frontend 
npm install

# 5. Inicializar el proyecto Django
# (Solo si el proyecto aún no ha sido creado)
django-admin startproject evory_drive .

# 6. Crear las migraciones (estructura de la base de datos)
python manage.py makemigrations

# 7. Aplicar las migraciones a la base de datos
python manage.py migrate

# 8. Crear un superusuario para acceder al panel de administración
python manage.py createsuperuser

# 9. Iniciar el servidor de desarrollo
python manage.py runserver

# 10. Acceder a la ruta para registro de conductores:
# URL del endpoint local
http://127.0.0.1:8000/registro-conductores/

#11 Formulario de Registro de Clientes
http://127.0.0.1:8000/registro-cliente/

 Panel de Administración Django
http://127.0.0.1:8000/admin/