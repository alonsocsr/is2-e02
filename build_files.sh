echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv

# activate the virtual environment
source venv/bin/activate

# Instalar dependencias
pip install -r requirements_vercel.txt || { echo "Error al instalar dependencias"; exit 1; }

# Recopilar archivos estáticos
python3.9 manage.py collectstatic --noinput --clear || { echo "Error al recopilar archivos estáticos"; exit 1; }

echo "BUILD END"