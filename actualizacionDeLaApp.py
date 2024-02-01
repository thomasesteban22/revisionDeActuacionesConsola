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
        # Descargar la actualización
        update_url = "https://github.com/thomasesteban22/revisionDeActuacionesConsola/releases/download/" + available_version + "/update.zip"
        update_file = requests.get(update_url).content

        # Verificar el tamaño del archivo de actualización
        if len(update_file) == 0:
            print("El archivo de actualización está vacío.")
            return


        # Descomprimir la actualización
        try:
            with open("update.zip", "wb") as f:
                f.write(update_file)

            with zipfile.ZipFile("update.zip", "r") as zip_ref:
                zip_ref.extractall()
        except Exception as e:
            print("Error al descargar o descomprimir la actualización:", e)
            return

        # Instalar la actualización
        print("¿Desea instalar la actualización? (s/n)")
        answer = input()
        if answer == "s":
            with zipfile.ZipFile("update.zip", "r") as zip_ref:
                zip_ref.extractall()
    else:
        print("No hay actualizaciones disponibles.")
