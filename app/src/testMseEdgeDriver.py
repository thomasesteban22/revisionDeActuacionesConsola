from selenium import webdriver
from selenium.webdriver.edge.service import Service

def ejecutar_test():
    msedge_driver_path = r'/msedgedriver.exe'

    service = Service(executable_path=msedge_driver_path, verbose=True, log_path='../file.log')
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')

    try:
        driver = webdriver.Edge(service=service, options=options)
        driver.get('https://www.google.com')
        print("Página cargada exitosamente.")
        driver.quit()
    except Exception as e:
        print(f"Error al iniciar Edge: {e}")

if __name__ == "__main__":
    ejecutar_test()
