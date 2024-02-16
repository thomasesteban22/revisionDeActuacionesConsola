from Actualizaciones import check_update as check_update
import subprocess
import os

def main():
    
    with open("revisionDeActuacionesConsola/version.txt", "r") as f:
        versionActual = f.read().strip()
    versionActualStr = str(versionActual) 
    print(versionActualStr)
    try:
        check_update()
    except:
        print("Error en la actualizacion")
        pass
    
    subprocess.run(["python", "revisionDeActuacionesConsola/src/main.py"])
main()