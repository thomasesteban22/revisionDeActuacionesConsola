from Actualizaciones import check_update as check_update

import subprocess


def main():
    try:
        check_update()
    except Exception as e:
        print(f"Error en la actualizacion: {e}")
        pass
    subprocess.run(["python", "revisionDeActuacionesConsola/src/main.py"])
main()