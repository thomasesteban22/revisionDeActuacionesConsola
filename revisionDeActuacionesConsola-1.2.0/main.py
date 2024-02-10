from Actualizaciones import check_update as check_update
import subprocess

def main():
    check_update()
    with open("version.txt", "r") as f:
        versionActual = f.read().strip()
    versionActualStr = str(versionActual)
    subprocess.run(["python", "revisionDeActuacionesConsola-" + versionActualStr + "/main.py"])
main()