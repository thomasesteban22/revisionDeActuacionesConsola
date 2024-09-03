from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import subprocess

app = Flask(__name__)
scheduler = BackgroundScheduler()


def print_current_time():
    colombia_tz = pytz.timezone('America/Bogota')
    current_time = datetime.now(colombia_tz).strftime("%Y-%m-%d %H:%M:%S")
    print(f"Hora actual en Bogotá, Colombia: {current_time}")


def scheduled_task():
    print(f"{datetime.now()}: Ejecutando la tarea programada...")
    try:
        subprocess.run(["python", "/app/src/main2.py"])  # Ejecutar el subproceso
        print("Subproceso ejecutado correctamente")
    except Exception as e:
        print(f"Error al ejecutar el subproceso: {e}")
    print(f"{datetime.now()}: Tarea programada completada.")


# Configura el trabajo programado
scheduler.add_job(scheduled_task, 'cron', hour=22, minute=59)
scheduler.start()


@app.route('/')
def home():
    return jsonify({"message": "Aplicación Flask en ejecución"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
