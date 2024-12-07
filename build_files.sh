set -o errexit

pip install -r requirements_.txt

python manage.py collectstatic --noinput --clear || { echo "Error al recopilar archivos estáticos"; exit 1; }
