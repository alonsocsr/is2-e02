#Se carga la imagen que contendrá el contenedor#

FROM python:3.11.4-slim-buster AS builder

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1	# Impide que python escriba archivos pyc en disco
ENV PYTHONUNBUFFERED 1	# Impide que python almacene en buffer stdout y stderr

# Directorio de trabajo
WORKDIR /app

# Instalacion de los requirements del proyecto
COPY ./requirements.txt . /app/
RUN pip install -r requirements.txt
COPY . /app/

ENTRYPOINT [ "sh", "-c", "./start.sh" ]