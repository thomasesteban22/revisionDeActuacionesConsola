import sys
import traceback
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import datetime
import locale
from datetime import date, timedelta
from datetime import datetime
from time import sleep

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging
import openpyxl

import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk

import termcolor
import time

options = webdriver.EdgeOptions()
    # Abre el navegador
driver = webdriver.Edge(options=options)

def loginEnTemis():
    usrCarlos = 79896136
    usrLady = 52754016
    passTemis = 12345
    
    try:
        driver.get("https://www.cisa.gov.co/TEMISWEB/Autenticacion/Login")
        driver.maximize_window()
    except:
        print("Error abiriendo la pagina de Temis")

    try:
        sleep(2)
        inputUsuario = driver.find_element(By.ID, "Usuario")
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", inputUsuario)
        inputUsuario.send_keys(usrCarlos)
        sleep(2)
        passUsuario = driver.find_element(By.ID, "Password")
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", passUsuario)
        passUsuario.send_keys(passTemis)
        sleep(2)
    except:
        print("Error encontrando el campo de usuario y clave")

    try:
        btnIngresar = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Ingresar']"))
    )
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", btnIngresar)
        btnIngresar.click()
        sleep(2)
    except:
        print("Error dando click en ingresar")

def dirigirseABuscarEnTemis():
    try:
        spanVigilanciaJudicial = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Vigilancia Judicial ']"))
        )
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", spanVigilanciaJudicial)
        spanVigilanciaJudicial.click()
        sleep(2)

    except:
        print("Error yendo a Vigilancia Judicial")

    try:
        aProcesosDeVigilanciaJ = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='Procesos de Vigilancia Judicial']"))
        )
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", aProcesosDeVigilanciaJ)
        aProcesosDeVigilanciaJ.click()
        sleep(2)
    except:
        print("Error yendo a procesos de vigilancia judicial")

def empezarABuscar():
    try:
        spanBuscarPor = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "slTipoBusqueda"))
        )
        spanSelecionado = Select(spanBuscarPor)
        spanSelecionado.select_by_value("0")
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", spanBuscarPor)
        sleep(2)
    except:
        print("encontrando el dropdown de buscar por")

    
    try:
        inputValorTemis = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "txtValorFiltro"))
        )
        inputValorTemis.send_keys("163102")
    except:
        print("Error colocando el numero de temis en el input")

    try:
        btnBuscar = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()=' Buscar']"))
    )   
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", btnBuscar)
        btnBuscar.click()

    except:
        print("Error dando click en boton buscar")


    sleep(5)
    # Buscar todos los botones en la página
    botones = driver.find_elements(By.TAG_NAME, "button")

    # Seleccionar el tercer botón
    btn_tercero = botones[2]
    driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", btn_tercero)
    driver.execute_script("arguments[0].click();", btn_tercero)
    sleep(5)

    try:
        aSeguimiento = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//a[@id='fLlnkSeguimiento']"))
        )
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", aSeguimiento)
        aSeguimiento.click()
    except:
        print("error encontrando el link seguimiento")

    try:
        btnAgregarSeguimiento = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()=' Agregar Seguimiento']"))
    )   
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", btnAgregarSeguimiento)
        btnAgregarSeguimiento.click()
    except:
        print("Error dando click en boton buscar")

   
    try:
        textAreaSeguimiento = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='Observacion']"))
        )
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", textAreaSeguimiento)
        textAreaSeguimiento.send_keys("Test")
        sleep(7)
    except:
        print("No se encontro el text area observaciones")
        
    
    try:
        btnGuardarSeguimiento = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='bntGuardarSeguimiento']"))
        )
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", btnGuardarSeguimiento)
        sleep(7)
    except:
        print("No se encontro el boton guardar -> segumiento")
        
    
    try:
        spanErrorCarga = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='FechaSeguimiento-error']"))
        )
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", spanErrorCarga)
        if(spanErrorCarga.is_displayed):
            print("Error de carga")
            driver.refresh()
            sleep(5)
        else:
            print("No hubo error")
        sleep(7)
    except:
        print("Hubo error en la carga de la fecha del seguimiento")
        pass

    

def seguimiento():
    loginEnTemis()
    dirigirseABuscarEnTemis()
    empezarABuscar()
    
seguimiento()

