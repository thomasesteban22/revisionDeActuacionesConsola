from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def main():
    chrome_driver_path = r'chromedriver.exe'

    service = Service(executable_path=chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://www.google.com')
        print("Página cargada exitosamente.")
        driver.quit()
    except Exception as e:
        print(f"Error al iniciar Chrome: {e}")


if __name__ == "__main__":
    main()
