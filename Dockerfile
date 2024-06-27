# Usa una imagen base oficial de Python
FROM python:3.12.1-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta 'revisionDeActuacionesConsola/app' al contenedor
COPY ./app /app

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Establece el comando para ejecutar la aplicación con Waitress
CMD ["waitress-serve", "--listen", "0.0.0.0:5000", "main:app"]
