from flask import Flask
import threading
import time
import schedule
import subprocess
from Actualizaciones import check_update as check_update

app = Flask(__name__)

print("Ejecutado el archivo main")

def scheduled_task():
    print("Ejecutando la tarea programada...")
    try:
        check_update()
    except Exception as e:
        print(f"Error en la actualizacion: {e}")
    subprocess.run(["python", "app/src/main.py"])
    print("Tarea programada completada.")

# Programar la tarea para que se ejecute todos los días a las 16:00 (4:00 PM)
schedule.every().day.at("23:48").do(scheduled_task)

# Función para ejecutar la planificación en segundo plano
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Ruta de prueba para verificar que la aplicación está en funcionamiento
@app.route('/')
def index():
    return "La aplicación está en funcionamiento y la tarea está programada."

if __name__ == "__main__":
    # Iniciar la ejecución del planificador en segundo plano
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # No es necesario ejecutar Waitress aquí, esto se manejará desde el Dockerfile
