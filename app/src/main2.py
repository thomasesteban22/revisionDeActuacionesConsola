import locale
import logging
import os
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, date, timedelta
import time
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import openpyxl

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

diasDeBusqueda = 5

# Ruta al controlador msedgedriver.exe
service = Service(executable_path='/usr/bin/chromedriver')  # Ruta común en Linux


def guardadoDeLogs(fInicio, fFinal, numRegistrosEscaneados):
    logger.info("Fecha Inicio: %s", fInicio.strftime("%d/%m/%Y %H:%M:%S"))
    logger.info("Fecha Final: %s", fFinal.strftime("%d/%m/%Y %H:%M:%S"))
    logger.info("Registros Escaneados: %d", numRegistrosEscaneados)


def obtenerFechaDeHoy():
    try:
        fechaHoy = datetime.now()
        print(f"Fecha de hoy obtenida: {fechaHoy}", flush=True)
        return fechaHoy
    except Exception as e:
        print("Error obteniendo la fecha de hoy, posible fallo de internet", flush=True)
        return None


def recorrerElExcel():
    try:
        if not os.path.exists("/app/data"):
            print("El directorio /app/data no existe.", flush=True)
            return

        archivo_path = "/app/data/informacion.txt"
        try:
            with open(archivo_path, "a") as archivoActuaciones:
                archivoActuaciones.write("\n")
                archivoActuaciones.flush()
                print(f"Archivo {archivo_path} abierto y limpiado correctamente.", flush=True)
        except IOError as e:
            print(f"No se pudo abrir o escribir en el archivo {archivo_path}: {e}", flush=True)
            return

        wb = openpyxl.load_workbook("/app/src/FOLDERESBASENUEVA.xlsm")
        ws = wb["CONSULTA UNIFICADA DE PROCESOS"]
        print("Archivo Excel abierto correctamente.", flush=True)
    except Exception as e:
        print(f"Error abriendo el Excel: {e}", flush=True)
        return

    n_filas = ws.max_row
    print(f"Número de filas en la hoja de trabajo: {n_filas}", flush=True)

    try:
        for fila in range(2, n_filas + 1):
            valor = ws['B' + str(fila)].value
            numeroDeProceso = valor
            if valor is None or valor == "":
                continue
            else:
                revisarActuaciones(numeroDeProceso)
    except Exception as e:
        print(f"Error en recorrer el Excel: {e}", flush=True)

    try:
        with open(archivo_path, "a") as archivoActuaciones:
            archivoActuaciones.write("\n")
            archivoActuaciones.write("######################################\n")
            archivoActuaciones.write(f"# REGISTROS ESCANEADOS: {fila - 1} DE: {n_filas}\n")
            archivoActuaciones.write("######################################\n")
            archivoActuaciones.flush()
            print(f"Información añadida al archivo {archivo_path}.", flush=True)
    except Exception as e:
        print(f"Error escribiendo en el archivo de información: {e}", flush=True)


def revisarActuaciones(numeroDeProceso):
    print(f"Revisando actuaciones para el proceso: {numeroDeProceso}", flush=True)

    fechaHoy = obtenerFechaDeHoy()
    if fechaHoy is None:
        print("No se pudo obtener la fecha de hoy. Saliendo de la función.", flush=True)
        return

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)

    while True:
        try:
            time.sleep(5)
            driver.get("https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion")
            time.sleep(1)
            print("Página cargada exitosamente.", flush=True)
            break
        except Exception as e:
            print(f"Error al cargar la página: {e}. Reintentando...", flush=True)
            driver.refresh()
            time.sleep(300)
            if not driver.window_handles:
                print("Se detuvo el escaneo de registros manualmente.", flush=True)
                break

    try:
        div_elements = driver.find_elements(By.CSS_SELECTOR, "div.v-input--selection-controls__input")
        second_div_element = div_elements[2]
        second_div_element.click()

        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Ingrese los 23 dígitos del número de Radicación']")
            )
        )
        time.sleep(1)
        element.send_keys(numeroDeProceso)
        print(f"Número de radicación ingresado: {element.get_attribute('value')}", flush=True)

        span_consultar = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Consultar']"))
        )
        time.sleep(1)
        span_consultar.click()

        try:
            boton_volver = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()=' Volver ']"))
            )
            if boton_volver:
                boton_volver.click()
                print("Botón 'Volver' encontrado y clickeado.", flush=True)
        except TimeoutException:
            print("No hay span 'Volver'.", flush=True)
            pass

        tablas = WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        resTablaFechaAC = tablas[0]
        for fila in resTablaFechaAC.find_elements(By.TAG_NAME, "tr"):
            if len(fila.find_elements(By.TAG_NAME, "td")) > 0:
                celdaFecha = fila.find_elements(By.TAG_NAME, "td")[2]
                botonFecha = celdaFecha.find_element(By.TAG_NAME, "button")
                if botonFecha:
                    fechaInicialComparar = date.fromisoformat(botonFecha.text)
                    fechaInicialStr = fechaInicialComparar.strftime("%Y-%m-%d")
                    for i in range(0, diasDeBusqueda):
                        fechaTemporalComprar = fechaHoy - timedelta(days=i)
                        fechaTemporalComprar = fechaTemporalComprar.strftime("%Y-%m-%d")
                        if fechaInicialStr == fechaTemporalComprar:
                            print(f"Fecha encontrada en el rango: {fechaInicialStr}", flush=True)
                            botonFecha.click()
                            break
                    else:
                        print(f"Fecha {fechaInicialStr} no está en el rango de búsqueda.", flush=True)
    except Exception as e:
        print(f"Error en la búsqueda de tabla: {e}", flush=True)
        pass

    try:
        tablas = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        time.sleep(1)
        tabla_actuaciones = tablas[1]

        for fila in tabla_actuaciones.find_elements(By.TAG_NAME, "tr"):
            if len(fila.find_elements(By.TAG_NAME, "td")) > 0:
                celdaFecha = fila.find_elements(By.TAG_NAME, "td")[0]
                fechaObtenida = date.fromisoformat(celdaFecha.text)
                actuacionObtenida = fila.find_elements(By.TAG_NAME, "td")[1].text
                anotacionObtenida = fila.find_elements(By.TAG_NAME, "td")[2].text
                fechaObtenida_str = fechaObtenida.strftime("%Y-%m-%d")

                for i in range(0, diasDeBusqueda):
                    fecha_comparacion = fechaHoy - timedelta(days=i)
                    fecha_comparacion = fecha_comparacion.strftime("%Y-%m-%d")
                    if fechaObtenida_str == fecha_comparacion:
                        with open("/app/data/informacion.txt", "a") as archivoActuaciones:
                            archivoActuaciones.write("\n")
                            archivoActuaciones.write(f"NUMERO DEL PROCESO: {numeroDeProceso}\n")
                            archivoActuaciones.write(f"Fecha: {fechaObtenida_str}\n")
                            archivoActuaciones.write(f"Actuacion: {actuacionObtenida}\n")
                            archivoActuaciones.write(f"Anotacion: {anotacionObtenida}\n")
                            archivoActuaciones.write(
                                "-----------------------------------------------------------------\n")
                        print(f"Información guardada para la fecha: {fechaObtenida_str}", flush=True)
    except Exception as e:
        print(f"No se realizó la búsqueda de actuaciones: {e}", flush=True)
        pass
    finally:
        driver.quit()


def enviarArchivoCorreo():
    fecha_ahora = datetime.now()
    fechaHoyStr = fecha_ahora.strftime("%A %d - %m - %Y a las %I:%M %p").capitalize()

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    correo_emisor = "registroautomaticoactuaciones@gmail.com"
    correo_receptor = "registroautomaticoactuaciones@gmail.com"
    asunto = "Registro escaneo de documento desde el servidor"

    archivo_adjuntar = "/app/data/informacion.txt"

    smtp.login(correo_emisor, "lctc zggr fztd eokc")

    mensaje = MIMEMultipart()
    mensaje["Subject"] = asunto
    mensaje["From"] = correo_emisor
    mensaje["To"] = correo_receptor

    cuerpo = f"Correo Auto-Registros de {fechaHoyStr}\n"
    mensaje.attach(MIMEText(cuerpo))

    with open(archivo_adjuntar, "rb") as archivo:
        archivo_adjunto = MIMEApplication(archivo.read())
        archivo_adjunto.add_header('Content-Disposition', 'attachment', filename=archivo_adjuntar)
        mensaje.attach(archivo_adjunto)

    smtp.sendmail(correo_emisor, correo_receptor, mensaje.as_string())
    smtp.quit()
    print("Correo enviado exitosamente.", flush=True)


def main():
    try:
        fechaHoy = obtenerFechaDeHoy()
        fechaFinal = fechaHoy

        recorrerElExcel()

        guardadoDeLogs(fechaHoy, fechaFinal, 10)

        enviarArchivoCorreo()

    except Exception as e:
        print(f"Error en el main: {e}", flush=True)


if __name__ == "__main__":
    main()
