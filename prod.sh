#!/bin/sh
DJANGO_SETTINGS_MODULE="cms.settings.prod"  # Cambia según sea necesario
PROJECT_NAME="is2-e02"  # Nombre de la carpeta raíz de tu proyecto

# Obtener el directorio donde se encuentra el script
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Directorio del proyecto
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="venv"

# Crear y activar el entorno virtual
echo "Creando entorno virtual..."
python3 -m venv $VENV_DIR
. $VENV_DIR/bin/activate

# Instalar dependencias 
echo "Instalando dependencias..."
pip install -r $PROJECT_DIR/requirements.txt

# Aplicar migraciones y colectar archivos estáticos
echo "Aplicando migraciones y colectando archivos estáticos..."
python manage.py migrate --settings=$DJANGO_SETTINGS_MODULE
python3 manage.py collectstatic --settings=$DJANGO_SETTINGS_MODULE

#Copiamos los archivos estaticos generado en el paso anterior a la carpeta static para que nginx pueda servirlos

# Cargamos los datos iniciales 
python3 manage.py loaddata fixtures/users.json --settings=$DJANGO_SETTINGS_MODULE
python3 manage.py loaddata fixtures/profiles.json --settings=$DJANGO_SETTINGS_MODULE
python3 manage.py loaddata fixtures/categorias.json --settings=$DJANGO_SETTINGS_MODULE

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl enable gunicorn

sudo systemctl restart nginx

#gunicorn --workers 3 --bind 0.0.0.0:8000 cms.wsgi:application

