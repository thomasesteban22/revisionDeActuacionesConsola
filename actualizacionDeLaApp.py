import os
import requests
import zipfile

def check_update():
    # Obtener la versión actual de la aplicación
    current_version = "1.0.0"

    # Obtener la versión de la actualización disponible
    response = requests.get("https://api.github.com/repos/thomasesteban22/revisionDeActuacionesConsola/releases/latest").json()
    available_version = response.get("tag_name")

    # Si la versión disponible es superior a la versión actual, descargar la actualización
    if available_version is not None and available_version > current_version:
        # Descargar el archivo de actualización
        update_url = "https://github.com/thomasesteban22/revisionDeActuacionesConsola/archive/refs/tags/" + available_version + ".zip"

        # Verificar si el archivo de actualización existe
        head_response = requests.head(update_url)
        if head_response.status_code == 404:
            print("El archivo de actualización no existe.")
            return

        # Guardar el archivo de actualización en el disco como un archivo binario
        with open("update.zip", "wb") as f:
            f.write(requests.get(update_url).content)

        # Try to unzip the update file
        try:
            with zipfile.ZipFile("update.zip", "r") as zip_ref:
                zip_ref.extractall()
        except Exception as e:
            print("Error al descargar o descomprimir la actualización:", e)
            return

        # Instalar la actualización
        print("¿Desea instalar la actualización? (s/n)")
        answer = input()
        if answer == "s":
            # Reemplazar el código actual por el código nuevo
            filename = os.path.basename("revisionDeActuacionesSinInterfaz")
            if os.path.exists(filename):
                os.rename(filename, "revisionDeActuacionesConsola-1.1.0")
            else:
                print("El archivo 'revisionDeActuacionesConsola' no existe.")
    else:
        print("No hay actualizaciones disponibles.")