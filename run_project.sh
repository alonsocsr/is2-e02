#!/bin/sh
DB_USER="starkuser"
DB_PASSWORD="starkpass"
REPO_URL="https://github.com/alonsocsr/is2-e02.git"
ENV_FILE="$(dirname "$(realpath "$0")")/.env"

# Pedir al usuario que elija el entorno (desarrollo o producción)
echo "Selecciona el entorno a ejecutar:"
echo "1) Desarrollo"
echo "2) Producción"
read -p "Ingresa el número correspondiente (1 o 2): " ENV_OPTION

if [ "$ENV_OPTION" = "1" ]; then
    DJANGO_SETTINGS_MODULE="cms.settings.dev"
    DB_NAME="starkdevdb"

elif [ "$ENV_OPTION" = "2" ]; then
    DJANGO_SETTINGS_MODULE="cms.settings.prod"
    DB_NAME="starkproddb"
else
    echo "Opción no válida. Saliendo del script."
    exit 1
fi

# Selección de tag
echo "Selecciona el tag que deseas utilizar:"
echo "1) v1"        
echo "2) v2"
echo "3) v3"
echo "4) v4"
echo "5) v5"
echo "6) v6"
read -p "Ingresa el número correspondiente (1-6) o presiona Enter para usar 'main': " TAG_OPTION

if [ "$TAG_OPTION" = "1" ]; then
    TAG="v1"
    PROJECT_NAME="is2-e02-v1"
elif [ "$TAG_OPTION" = "2" ]; then
    TAG="v2"
    PROJECT_NAME="is2-e02-v2"
elif [ "$TAG_OPTION" = "3" ]; then
    TAG="v3"
    PROJECT_NAME="is2-e02-v3"
elif [ "$TAG_OPTION" = "4" ]; then
    TAG="v4"
    PROJECT_NAME="is2-e02-v4"
elif [ "$TAG_OPTION" = "5" ]; then
    TAG="v5"
    PROJECT_NAME="is2-e02-v5"
elif [ "$TAG_OPTION" = "6" ]; then
    TAG="v6"
    PROJECT_NAME="is2-e02-v6"
else
    TAG="main"
    PROJECT_NAME="is2-e02-main"
fi

# Actualizar e instalar dependencias base
echo "Actualizando paquetes..."
sudo systemctl stop unattended-upgrades
sudo systemctl stop apparmor

# Instalar git
echo "Instalando Git..."
sudo apt-get install -y git

# Clonar el repositorio
echo "Clonando repositorio..."
git clone --branch $TAG --depth 1 $REPO_URL $PROJECT_NAME
cp "$ENV_FILE" "$PROJECT_NAME/.env"
cd $PROJECT_NAME

# Instalar Python y herramientas necesarias
echo "Instalando Python y pip..."
sudo apt install -y python3-pip python3.12-venv

# Instalar PostgreSQL y crear la base de datos
echo "Instalando PostgreSQL y configurando la base de datos..."
sudo apt install -y postgresql postgresql-contrib
sudo service postgresql start

# Configuración de PostgreSQL
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

# Otorgar permisos en la base de datos específica
sudo -u postgres psql -d $DB_NAME << EOF
GRANT USAGE ON SCHEMA public TO $DB_USER;
ALTER SCHEMA public OWNER TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;
EOF

# Crear y activar el entorno virtual
echo "Creando entorno virtual..."
python3 -m venv venv
. venv/bin/activate

# Instalar dependencias 
echo "Instalando dependencias..."
PROJECT_DIR=$(dirname "$(realpath "$0")")
pip install -r $PROJECT_DIR/requirements.txt

# Si el entorno es de producción
if [ "$ENV_OPTION" = "2" ]; then
    # Instalar Nginx y Gunicorn
    echo "Instalando Nginx y Gunicorn..."
    sudo apt install -y nginx
    pip install -y gunicorn

    # Configuración de Gunicorn y Nginx
    echo "Configurando Gunicorn y Nginx..."

    # Crear el archivo de configuración de Gunicorn
    sudo tee /etc/systemd/system/gunicorn.service > /dev/null << EOF
    [Unit]
    Description=gunicorn daemon
    Before=nginx.service
    After=network.target

    [Service]
    User=$USER
    Group=www-data
    WorkingDirectory=$(pwd)
    Environment="DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE"
    ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock cms.wsgi:application

    [Install]
    WantedBy=multi-user.target
EOF

    sudo tee /etc/systemd/system/gunicorn.socket > /dev/null << EOF
    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target
EOF

    # Configuración de Nginx
    sudo tee /etc/nginx/sites-available/cms > /dev/null << EOF
    server {
        listen 80;
        server_name localhost;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            alias $(pwd)/staticfiles/;
            autoindex on;
        }

        location /files/ {
            alias $(pwd)/uploads/;
            autoindex on;
        }

        location / {
            proxy_pass http://unix:/run/gunicorn.sock;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
EOF

    sudo ln -s /etc/nginx/sites-available/cms /etc/nginx/sites-enabled

    # Aplicar migraciones y colectar archivos estáticos
    echo "Aplicando migraciones y colectando archivos estáticos..."
    python manage.py migrate --settings=$DJANGO_SETTINGS_MODULE
    python3 manage.py collectstatic --settings=$DJANGO_SETTINGS_MODULE --noinput
    
    #Permisos de lectura y escritura para los statics
    sudo chmod 775 -R /home/$USER/

    # Cargamos los datos iniciales
    python3 manage.py loaddata fixtures/users.json --settings=$DJANGO_SETTINGS_MODULE
    python3 manage.py loaddata fixtures/profiles.json --settings=$DJANGO_SETTINGS_MODULE

    # Otorgar permisos
    echo "Otorgando permisos..."
    sudo chown root:www-data /run
    sudo chmod 775 /run

    # Reiniciar y habilitar servicios
    sudo systemctl daemon-reload
    sudo systemctl restart nginx
    sudo systemctl restart gunicorn
    sudo systemctl enable gunicorn

# Si el entorno es de desarrollo
elif [ "$ENV_OPTION" = "1" ]; then
    # Aplicar migraciones
    echo "Aplicando migraciones"
    python manage.py makemigrations --settings=$DJANGO_SETTINGS_MODULE
    python manage.py migrate --settings=$DJANGO_SETTINGS_MODULE

    # Cargamos los datos iniciales 
    python3 manage.py loaddata fixtures/users.json --settings=$DJANGO_SETTINGS_MODULE
    python3 manage.py loaddata fixtures/profiles.json --settings=$DJANGO_SETTINGS_MODULE
    python3 manage.py loaddata fixtures/categorias.json --settings=$DJANGO_SETTINGS_MODULE

    chmod +x documentation.sh
    chmod +x tests.sh

    python3 manage.py runserver
fi

echo "¡El proyecto se ha configurado y está corriendo correctamente!"
sudo systemctl start unattended-upgrades
