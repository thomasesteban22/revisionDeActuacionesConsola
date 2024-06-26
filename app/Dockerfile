# Usa una imagen base de Python 3.12.1
FROM python:3.12.1-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY ./app /app
COPY ./requirements.txt /app/requirements.txt

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Define el comando por defecto para ejecutar tu aplicación
CMD ["python", "main.py"]
