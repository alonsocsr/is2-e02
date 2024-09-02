#!/bin/sh

sudo systemctl stop gunicorn

DJANGO_SETTINGS_MODULE="cms.settings.dev"  # Cambia según sea necesario
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

# Cargamos los datos iniciales 
python3 manage.py loaddata fixtures/users.json --settings=$DJANGO_SETTINGS_MODULE
python3 manage.py loaddata fixtures/profiles.json --settings=$DJANGO_SETTINGS_MODULE
python3 manage.py loaddata fixtures/categorias.json --settings=$DJANGO_SETTINGS_MODULE

chmod +x documentation.sh
chmod +x tests.sh

# Corremos el proyecto
echo 'Iniciando Servidor'
python3 manage.py runserver


