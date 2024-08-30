import locale

from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import datetime
from datetime import date, timedelta
from datetime import datetime
from time import sleep

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging
import openpyxl

import time

diasDeBusqueda = 2

# Ruta al controlador msedgedriver.exe
msedge_driver_path = r'./msedgedriver.exe'


def guardadoDeLogs(fInicio, fFinal, numRegistrosEscaneados):
    logging.info("Fecha Inicio: %s", fInicio.strftime("%d/%m/%Y %H:%M:%S"))
    logging.info("Fecha Final: %s", fFinal.strftime("%d/%m/%Y %H:%M:%S"))
    logging.info("Registros Escaneados: %d", numRegistrosEscaneados)


def obtenerFechaDeHoy():
    try:
        fechaHoy = datetime.now()
        print(f"Fecha de hoy obtenida: {fechaHoy}")
        return fechaHoy
    except:
        print("Error obteniendo la fecha de hoy, posible fallo de internet")
        return None


def recorrerElExcel():
    try:
        # Abre el archivo Excel
        wb = openpyxl.load_workbook("src/FOLDERESBASENUEVA.xlsm")
        # Obtiene la hoja de trabajo activa
        ws = wb["CONSULTA UNIFICADA DE PROCESOS"]
        print("Archivo Excel abierto correctamente.")
    except:
        print("Error abriendo el Excel, verificar ruta y nombre del archivo")
        return

    # Obtiene el número de filas de la hoja de trabajo
    n_filas = ws.max_row
    print(f"Número de filas en la hoja de trabajo: {n_filas}")

    try:
        for fila in range(2, n_filas + 1):
            valor = ws['B' + str(fila)].value
            numeroDeProceso = valor
            if valor is None or valor == "":
                continue
            else:
                revisarActuaciones(numeroDeProceso)
    except Exception as e:
        print(f"Error en recorrer el Excel: {e}")
        pass

    archivoActuaciones = open(
        "data/informacion.txt", "a")
    archivoActuaciones.write("\n")

    indiceFila = fila - 1
    texto = f"# REGISTROS ESCANEADOS: {indiceFila} DE: {n_filas}\n"
    print(f"Registros escaneados: {indiceFila} de {n_filas}")

    archivoActuaciones.write("######################################\n")
    archivoActuaciones.write(texto)
    archivoActuaciones.write("######################################\n")
    archivoActuaciones.close()


def revisarActuaciones(numeroDeProceso):
    print(f"Revisando actuaciones para el proceso: {numeroDeProceso}")

    fechaHoy = obtenerFechaDeHoy()
    if fechaHoy is None:
        print("No se pudo obtener la fecha de hoy. Saliendo de la función.")
        return

    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Configurar el servicio para Edge
    service = Service(executable_path=msedge_driver_path)

    # Inicializa el navegador Edge utilizando el servicio configurado
    driver = webdriver.Edge(service=service, options=options)

    while True:
        try:
            sleep(5)
            driver.get("https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion")
            sleep(1)
            print("Página cargada exitosamente.")
            break
        except:
            driver.refresh()
            time.sleep(300)
            if not driver.window_handles:
                print("Se detuvo el escaneo de registros manualmente")
                break
            print("Error al cargar la página, posible fallo de internet")

    div_elements = driver.find_elements(By.CSS_SELECTOR, "div.v-input--selection-controls__input")
    second_div_element = div_elements[2]
    second_div_element.click()

    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Ingrese los 23 dígitos del número de Radicación']"))
    )
    sleep(1)
    element.send_keys(numeroDeProceso)
    print(f"Número de radicación ingresado: {element.get_attribute('value')}")

    span_consultar = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Consultar']")))
    sleep(1)
    span_consultar.click()

    try:
        boton_volver = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()=' Volver ']"))
        )
        if boton_volver:
            boton_volver.click()
            print("Botón 'Volver' encontrado y clickeado.")
    except:
        print("No hay span 'Volver'")
        pass

    try:
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
                            print(f"Fecha encontrada en el rango: {fechaInicialStr}")
                            botonFecha.click()
                            break
                    else:
                        print(f"Fecha {fechaInicialStr} no está en el rango de búsqueda.")
    except Exception as e:
        print(f"Error en la búsqueda de tabla: {e}")
        pass

    try:
        tablas = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        sleep(1)
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
                        with open(
                                "../../../../Escritorio/revisionDeActuacionesConsola/revisionDeActuacionesConsola/src/informacion.txt",
                                "a") as archivoActuaciones:
                            archivoActuaciones.write("\n")
                            archivoActuaciones.write(f"NUMERO DEL PROCESO: {numeroDeProceso}\n")
                            archivoActuaciones.write(f"Fecha: {fechaObtenida_str}\n")
                            archivoActuaciones.write(f"Actuacion: {actuacionObtenida}\n")
                            archivoActuaciones.write(f"Anotacion: {anotacionObtenida}\n")
                            archivoActuaciones.write(
                                "-----------------------------------------------------------------\n")
                        print(f"Información guardada para la fecha: {fechaObtenida_str}")
    except Exception as e:
        print(f"No se realizó la búsqueda de actuaciones: {e}")
        pass
    finally:
        driver.quit()


def enviarArchivoCorreo():
    fecha_ahora = datetime.now()
    locale.setlocale(locale.LC_ALL, 'es_ES')
    fechaHoyStr = fecha_ahora.strftime("%A %d - %m - %Y a las %I:%M %p").capitalize()

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    correo_emisor = "registroautomaticoactuaciones@gmail.com"
    correo_receptor = "registroautomaticoactuaciones@gmail.com"
    asunto = "Registro escaneo de documento"

    archivo_adjuntar = "informacion.txt"

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
    print("Correo enviado exitosamente.")


def main():
    try:
        fechaHoy = obtenerFechaDeHoy()
        fechaFinal = fechaHoy

        recorrerElExcel()

        guardadoDeLogs(fechaHoy, fechaFinal, 10)

        #enviarArchivoCorreo()

    except Exception as e:
        print(f"Error en el main: {e}")


if __name__ == "__main__":
    main()
