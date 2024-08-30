#!/bin/sh

# Realizamos las migraciones
echo 'Iniciando Migraciones'
python manage.py makemigrations
python manage.py migrate

# Cargamos los datos iniciales
# python manage.py loaddata fixtures/categorias.json

# Corremos el proyecto
echo 'Iniciando Servidor'
python manage.py runserver 0.0.0.0:8000