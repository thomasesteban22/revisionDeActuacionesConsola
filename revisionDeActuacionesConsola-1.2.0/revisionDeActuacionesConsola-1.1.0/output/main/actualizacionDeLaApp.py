import requests
import zipfile

def check_update():
    # Obtener la versión actual de la aplicación
    current_version = "1.0.0"

    # Obtener la versión de la actualización disponible
    available_version = requests.get("https://api.github.com/repos/thomasesteban22/revisionDeActuacionesConsola/releases/latest").json()["tag_name"]

    # Si la versión disponible es superior a la versión actual, descargar la actualización
    if available_version > current_version:
        # Descargar la actualización
        update_url = "https://github.com/thomasesteban22/revisionDeActuacionesConsola/releases/download/" + available_version + "/update.zip"
        update_file = requests.get(update_url).content

        # Descomprimir la actualización
        with open("update.zip", "wb") as f:
            f.write(update_file)

        # Instalar la actualización
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall()