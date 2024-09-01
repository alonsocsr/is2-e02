#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

set -e

# Realizamos las migraciones
python manage.py makemigrations
python manage.py migrate

# Cargamos los datos iniciales
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/profiles.json
python manage.py loaddata fixtures/categorias.json

# Recoleta todos los archivos estaticos de todas las app y los agrupa en una carpeta staticfiles
python manage.py collectstatic --noinput

gunicorn project.wsgi -b 0.0.0.0:8000
