# Usa una imagen base oficial de Python
FROM python:3.12.1-slim

# Instala dependencias necesarias para Chrome y Chromedriver
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    wget \
    xdg-utils \
    locales \
    --no-install-recommends

# Establece el locale directamente en el Dockerfile
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES:es
ENV LC_ALL es_ES.UTF-8

# Genera la configuración regional
RUN locale-gen es_ES.UTF-8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta 'app' al contenedor
COPY ./app /app

# Expone el puerto en el que la aplicación Flask correrá
EXPOSE 5000

# Establece el comando para ejecutar la aplicación con Waitress
CMD ["waitress-serve", "--listen=0.0.0.0:5000", "main:app"]
