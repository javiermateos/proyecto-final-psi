# Notes

Este archivo contiene los comandos necesarios así como las anotaciones
para realizar la práctica y el examen de enero.

## Django 

1. Creación del proyecto y la aplicación.
```shell
virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
django-admin.py startproject labassign
cd labassign
python manage.py startapp core
```
2. Creacion de directorios y archivos necesarios.

Desde el directorio del proyecto django, es decir, desde dentro de la carpeta labassign ejecutamos:
```sh
touch test_query.py
mkdir -p core/labassign/management/commands/
touch core/labassign/management/commands/populate.py
mkdir static
mkdir templates
```
3. Configuración del proyecto django en settings.py
```python
import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

INSTALLED_APPS = [
    "core",
]


TEMPLATES = [
  {
    "DIRS": [TEMPLATE_DIR],
  },
]

DATABASES = {
    "default":
    dj_database_url.config(
        default="postgres://alumnodb:alumnodb@localhost:5432/psi")
}
if os.getenv("SQLITE", False):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }


TIME_ZONE = "Europe/Madrid"

STATIC_ROOT = os.path.join(BASE_DIR, "staticHeroku")

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    STATIC_DIR,
]
```
A partir de aquí habría que codificar en el siguiente orden las cosas:

- Crear los modelos en models.py
- Añadir los modelos en admin.py
- Crear el archivo populate.py
- Añadir las vistas en views.py
- Añadir las vistas a las urls.py
- Crear los archivos html de las templates
- Pasar los test
- Hacer el deploy en Heroku

## PostgreSQL

1. Comprobación del servicio de postgresql.
```sh
sudo systemctl status postgresql.service
sudo systemctl start postgresql.service
```
Nota: Si no quieres iniciar postgresql cada vez que quieras conectarte debes
habilitarlo con el comando: 
```sh
sudo systemctl enable postgresql.service
```
2. Creacion del usuario
```sh
sudo -iu postgres 
createuser --interactive # Crear usuario alumnodb:alumnodb
```
3. Creacion de la base de datos.
```sh
createdb -O alumnodb psi
```
## Heroku

1. Archivos necesarios en Heroku

- Procfile
- runtime.txt
- requirements.txt
- git local repository

2. Modificar variables del proyecto django en settings.py
```python
SECRET_KEY = os.environ.get("SECRET_KEY")
```
3. Modificar el archivo wsgi.py en la carpeta labassign
```python
from dj_static import Cling

application = Cling(get_wsgi_application())
```
2. Pasos necesarios para hacer el deploy en Heroku

Para ello es necesario situarse dentro de la carpeta del proyecto django. En este caso
sería la carpeta labassign (la primera).
```sh
git init
git add .
git commit -m "Repositorio local para heroku"
make config_heroku #Recuerda modificar el nombre de la app de heroku en el makefile
# Añadir a la variable ALLOWED HOST la direccion de heroku devuelta
heroku config:set SECRET_KEY=<valor>
make push_heroku
```
```python
ALLOWED_HOSTS = [
    u"<pagina_heroku>",
    u"localhost",
    u"127.0.0.1",
]
```
3. Pasos para realizar los test en heroku
```sh
make test_heroku
```
