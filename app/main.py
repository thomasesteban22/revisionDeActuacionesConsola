from flask import Flask
from flask_apscheduler import APScheduler
import subprocess
from Actualizaciones import check_update as check_update

app = Flask(__name__)

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

def scheduled_task(): 
    print("Ejecutando la tarea programada...")
    try:
        check_update()
    except Exception as e:
        print(f"Error en la actualizacion: {e}")
    subprocess.run(["python", "app/src/main.py"])
    print("Tarea programada completada.")

# Programar la tarea para que se ejecute todos los días a las 12:00 PM hora local
@scheduler.task('cron', id='do_job_1', hour=15, minute=0)
def job1():
    scheduled_task()

@app.route('/')
def index():
    return "La aplicación está en funcionamiento y la tarea está programada."

if __name__ == "__main__":
    app.run(host='magnaabogados-revision-actuaciones.kfvjqf.easypanel.h', port=5000)
