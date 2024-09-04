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
        process = subprocess.Popen(
            ["python", "-u", "/app/src/main2.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Lee stdout y stderr en tiempo real
        for stdout_line in iter(process.stdout.readline, ""):
            logger.info(stdout_line.strip())
        for stderr_line in iter(process.stderr.readline, ""):
            logger.error(stderr_line.strip())

        process.stdout.close()
        process.stderr.close()
        process.wait()
        logger.info("Subproceso ejecutado correctamente")

    except Exception as e:
        logger.error(f"Error al ejecutar el subproceso: {e}")

    logger.info("Tarea programada completada")


def run_scheduler():
    while True:
        print_current_time()
        colombia_tz = pytz.timezone('America/Bogota')
        current_time = datetime.now(colombia_tz)
        if current_time.hour == 19 and current_time.minute == 16:
            scheduled_task()
        time.sleep(25)  # Sleep for 25 seconds


@app.route('/')
def index():
    return 'La aplicación de webscrapping está funcionando'


if __name__ == "__main__":
    threading.Thread(target=run_scheduler).start()
    #app.run(host='0.0.0.0', port=5000)
