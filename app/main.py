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
    subprocess.run(["python", "app/src/main.py"])
    print("Tarea programada completada.")

# Ruta de prueba para verificar que la aplicación está en funcionamiento
@app.route('/')
def index():
    return "La aplicación está en funcionamiento."

if __name__ == "__main__":
    # Ejecutar la tarea programada una vez al iniciar el script
    scheduled_task()

    # Ejecutar la aplicación Flask con Waitress (ya está ejecutándose en Docker)
    app.run(host='0.0.0.0', port=5000)
