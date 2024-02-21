from Actualizaciones import check_update as check_update
import crearExe as crearExe
import subprocess


def main():
    try:
        check_update()
        crearExe()
    except Exception as e:
        print(f"Error en la actualizacion: {e}")
        pass
    subprocess.run(["python", "revisionDeActuacionesConsola/src/main.py"])
main()