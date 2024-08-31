#!/bin/sh

# Realizamos las migraciones
echo 'Iniciando Migraciones'
python3 manage.py makemigrations
python3 manage.py migrate

# Cargamos los datos iniciales
# python manage.py loaddata fixtures/categorias.json

# Corremos el proyecto
echo 'Iniciando Servidor'
python3 manage.py runserver 0.0.0.0:8000