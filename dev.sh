#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
    sudo service postgresql restart
fi
# Realizamos las migraciones
echo 'Iniciando Migraciones'
python3 manage.py makemigrations
python3 manage.py migrate

# Cargamos los datos iniciales


python3 manage.py loaddata fixtures/users.json
python3 manage.py loaddata fixtures/profiles.json
python3 manage.py loaddata fixtures/categorias.json


# Corremos el proyecto
echo 'Iniciando Servidor'
python3 manage.py runserver