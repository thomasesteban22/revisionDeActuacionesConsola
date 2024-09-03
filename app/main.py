import time
from datetime import datetime
import pytz
import subprocess


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


def run_scheduler():
    while True:
        print_current_time()
        colombia_tz = pytz.timezone('America/Bogota')
        current_time = datetime.now(colombia_tz)
        if current_time.hour == 22 and current_time.minute == 59:
            scheduled_task()
        time.sleep(25)  # Sleep for 25 seconds


if __name__ == "__main__":
    run_scheduler()
