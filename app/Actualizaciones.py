import os
import requests
import zipfile
import shutil

def check_update():
    # Obtener la versión actual de la aplicación
    with open("app/version.txt", "r") as f:
        versionActual = f.read().strip()
    print("Version Actual: " + versionActual)

    # Obtener la versión de la actualización disponible
    response = requests.get("https://api.github.com/repos/thomasesteban22/app/releases/latest").json()
    available_version = response.get("tag_name")

    # Si la versión disponible es superior a la versión actual, descargar la actualización
    if available_version is not None and available_version > versionActual:
        print("Version Disponible: " + available_version)
        # Descargar el archivo de actualización
        with open("app/versionAnterior.txt", 'w') as versionAnteriorTxt:
            versionAnteriorTxt.write(versionActual)

        with open("app/version.txt", 'w') as versionTxt:
            versionTxt.write(str(available_version))
        update_url = "https://github.com/thomasesteban22/app/archive/refs/tags/" + available_version + ".zip"

        # Verificar si el archivo de actualización existe
        head_response = requests.head(update_url)
        if head_response.status_code == 404:
            print("El archivo de actualización no existe.")
            return

        # Guardar el archivo de actualización en el disco como un archivo binario
        with open("app/update.zip", "wb") as f:
            f.write(requests.get(update_url).content)


        # Try to unzip the update file
        try:
            with zipfile.ZipFile("app/update.zip", "r") as zip_ref:
                zip_ref.extractall()
        except Exception as e:
            print("Error al descargar o descomprimir la actualización:", e)
            return

        # Instalar la actualización
        print("¿Desea instalar la actualización? (s/n)")
        answer = input()
        if answer == "s":
            # Reemplazar el código actual de la carpeta (src) por el código nuevo
            filename = os.path.basename("app")
            if os.path.exists(filename):
                try:
                    shutil.rmtree("app/src")
                    dirActualizacion = "app-"+str(available_version)+"/app/src"
                    dirRoot = "app/src"
                    shutil.move(dirActualizacion, dirRoot)
                    os.remove("app/update.zip")
                    shutil.rmtree("app-"+ str(available_version))
                except:
                    print("error moviendo")
            else:
                print("No se encuentra el archivo base")
    else:
        print("No hay actualizaciones disponibles.")