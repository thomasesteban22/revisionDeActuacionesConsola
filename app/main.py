import logging
from flask import Flask
import time
from datetime import datetime
import pytz
import subprocess
import threading

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def print_current_time():
    colombia_tz = pytz.timezone('America/Bogota')
    current_time = datetime.now(colombia_tz).strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Hora actual en Bogotá, Colombia: {current_time}")


def scheduled_task():
    logger.info("Ejecutando la tarea programada...")
    try:
        result = subprocess.run(
            ["python", "-u", "/app/src/main2.py"],
            capture_output=True,
            text=True
        )
        # Log the stdout and stderr from main2.py
        logger.info(f"Subproceso stdout: {result.stdout}")
        logger.error(f"Subproceso stderr: {result.stderr}")
        logger.info("Subproceso ejecutado correctamente")
    except Exception as e:
        logger.error(f"Error al ejecutar el subproceso: {e}")
    logger.info("Tarea programada completada.")


def run_scheduler():
    while True:
        print_current_time()
        colombia_tz = pytz.timezone('America/Bogota')
        current_time = datetime.now(colombia_tz)
        if current_time.hour == 19 and current_time.minute == 3:
            scheduled_task()
        time.sleep(25)  # Sleep for 25 seconds


@app.route('/')
def index():
    return 'La aplicación de webscrapping está funcionando'


if __name__ == "__main__":
    threading.Thread(target=run_scheduler).start()
    #app.run(host='0.0.0.0', port=5000)
