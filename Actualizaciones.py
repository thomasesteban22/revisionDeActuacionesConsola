import os
import requests
import zipfile
import shutil

def check_update():
    # Obtener la versión actual de la aplicación
    with open("version.txt", "r") as f:
        versionActual = f.read().strip()
    print(versionActual)

    # Obtener la versión de la actualización disponible
    response = requests.get("https://api.github.com/repos/thomasesteban22/revisionDeActuacionesConsola/releases/latest").json()
    available_version = response.get("tag_name")

    # Si la versión disponible es superior a la versión actual, descargar la actualización
    if available_version is not None and available_version > versionActual:
        # Descargar el archivo de actualización
        with open("versionAnterior.txt", 'w') as versionAnteriorTxt:
            versionAnteriorTxt.write(versionActual)

        with open("version.txt", 'w') as versionTxt:
            versionTxt.write(str(available_version))
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
            with open("versionAnterior.txt", "r") as f:
                versionAnterior = f.read().strip()
            # Reemplazar el código actual por el código nuevo
            filename = os.path.basename("revisionDeActuacionesConsola-"+versionAnterior)
            if os.path.exists(filename):
                #os.remove("revisionDeActuacionesConsola-"+versionAnterior)
                shutil.rmtree("revisionDeActuacionesConsola-"+versionAnterior)
                os.remove("update.zip")
                os.replace(filename, "revisionDeActuacionesConsola-"+versionActual)
            else:
                print("El archivo 'revisionActuacionesSinInterfaz' no existe.")
    else:
        print("No hay actualizaciones disponibles.")