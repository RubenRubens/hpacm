FROM python:3.9
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Añade los credenciales de la base de datos
ADD postgres_user .
ADD postgres_psswd .