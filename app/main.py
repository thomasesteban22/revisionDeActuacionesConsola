from flask import Flask
import subprocess
from Actualizaciones import check_update as check_update

app = Flask(__name__)

def scheduled_task():
    print("Ejecutando la tarea programada...")
    try:
        check_update()
    except Exception as e:
        print(f"Error en la actualizacion: {e}")
    subprocess.run(["python", "src/main.py"])
    print("Tarea programada completada.")

# Ruta de prueba para verificar que la aplicación está en funcionamiento
@app.route('/')
def index():
    return "La aplicación está en funcionamiento."

if __name__ == "__main__":
    print("Ejecutado main.py")
    scheduled_task()

