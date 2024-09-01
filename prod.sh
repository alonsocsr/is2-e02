DJANGO_SETTINGS_MODULE="settings.dev"  # Cambia según sea necesario
PROJECT_NAME="is2-e02"  # Nombre de la carpeta raíz de tu proyecto

# Obtener el directorio donde se encuentra el script
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Directorio del proyecto
PROJECT_DIR="$SCRIPT_DIR/$PROJECT_NAME"
VENV_DIR="$PROJECT_DIR/venv"

# Crear y activar el entorno virtual
echo "Creando entorno virtual..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r $PROJECT_DIR/requirements.txt

# Aplicar migraciones y colectar archivos estáticos
echo "Aplicando migraciones y colectando archivos estáticos..."
python manage.py migrate --settings=$DJANGO_SETTINGS_MODULE
python manage.py collectstatic -no-input --ignore admin --settings=$DJANGO_SETTINGS_MODULE

