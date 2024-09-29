import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from DriverManager.LoginPage import LoginPage


class BrowserManager():
    def __init__(self, browser_type):
        """
        Inicializa el driver basado en el navegador seleccionado.

        :param browser_type: Tipo de navegador a usar. Acepta "chrome" y "firefox".

        :type browser_type: str

        :raises ValueError: Si el tipo de navegador no es soportado.
        """
        # Diccionario para mapear el navegador con el servicio y el driver correspondiente
        browser_mapping = {
            'chrome': (ChromeService, webdriver.Chrome, r"webdrivers/chromedriver.exe"),
            'firefox': (FirefoxService, webdriver.Firefox, r"webdrivers/geckodriver.exe")
        }

        # Convertir el input a minúsculas para asegurar la correspondencia
        browser_type = browser_type.lower()

        # Verificar si el navegador está soportado
        if browser_type in browser_mapping:
            service_class, driver_class, driver_path = browser_mapping[browser_type]
            self.service = service_class(executable_path=driver_path)
            self.driver = driver_class(service=self.service)
        else:
            raise ValueError("Navegador no soportado. Usa 'chrome' o 'firefox'.")

    def open_browser(self, url):
        """
        Abre la URL especificada y maximiza la ventana del navegador.

        :param url: URL que se va a abrir en el navegador.
        :type url: str
        """
        self.driver.get(url)
        self.driver.maximize_window()

    def close_browser(self):
        """
        Cierra el navegador y libera los recursos asociados.
        """
        self.driver.quit()

    def select_element(self, selector_type, selector, seconds):
        """
        Selecciona un elemento en la página web utilizando diferentes tipos de selectores.

        Espera a que el elemento sea visible y lo desplaza a la vista.

        :param selector_type: Acepta los valores 'xpath', 'id', 'css', 'name' y 'link'.
        :param selector: El valor del selector, como la expresión XPath, el ID, o el nombre del elemento.
        :param seconds: Segundos antes de pasar a la siguiente tarea.

        :type selector_type: str
        :type selector: str
        :type seconds: float

        :return: El WebElement seleccionado si se encuentra. Retorna None si no se encuentra el elemento.

        :raises TimeoutException: Si no se encuentra el elemento en el tiempo permitido.
        :raises NoSuchElementException: Si el elemento no se encuentra en el DOM.
        :raises StaleElementReferenceException: Si el elemento ya no es un referente válido en el DOM.
        """
        try:
            by_mapping = {
                'xpath': By.XPATH,
                'id': By.ID,
                'css': By.CSS_SELECTOR,
                'name': By.NAME,
                'link': By.PARTIAL_LINK_TEXT
            }

            if selector_type not in by_mapping:
                print(f"Error: Tipo de selector '{selector_type}' no es válido.")
                return None

            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((by_mapping[selector_type], selector))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(seconds)
            return element

        except TimeoutException:
            print(f"Timeout: No se pudo encontrar el elemento con selector: {selector} en el tiempo permitido.")
            return None

        except NoSuchElementException:
            print(f"Error: El elemento con selector: {selector} no fue encontrado en el DOM.")
            return None

        except StaleElementReferenceException:
            print(f"Error: El elemento con selector: {selector} ya no es un referente válido en el DOM.")
            return None

    def write(self, text, selector_type, selector, seconds):
        """
        Escribe el texto en un campo de entrada identificado por un selector.

        :param text: El texto que se va a ingresar en el campo de entrada.
        :param selector_type: Acepta los valores 'xpath', 'id', 'css', 'name' y 'link'.
        :param selector: El valor del selector para identificar el campo de entrada.
        :param seconds: Tiempo en segundos a esperar entre acciones.

        :type text: str
        :type selector_type: str
        :type selector: str
        :type seconds: float
        """
        element = self.select_element(selector_type, selector, seconds)
        element.clear()
        element.send_keys(text)
        time.sleep(seconds)

    def click(self, selector_type, selector, seconds):
        """
        Hace clic en un elemento identificado por un selector.

        :param selector_type: Acepta los valores 'xpath', 'id', 'css', 'name' y 'link'.
        :param selector: El valor del selector para identificar el elemento.
        :param seconds: Tiempo en segundos a esperar después de hacer clic.

        :type selector_type: str
        :type selector: str
        :type seconds: float
        """
        element = self.select_element(selector_type, selector, seconds)
        element.click()
        time.sleep(seconds)

    def login(self, loginpage, seconds):
        """
        Realiza el flujo de login usando los selectores y credenciales de LoginPage.

        :param loginpage: Objeto que contiene la URL y los selectores necesarios para el login.
        :param seconds: Tiempo en segundos a esperar entre acciones.

        :type loginpage: LoginPage
        :type seconds: float
        """
        self.open_browser(loginpage.url)
        self.write(loginpage.credentials.username, 'xpath', loginpage.username_selector, seconds)
        self.write(loginpage.credentials.pwd, 'xpath', loginpage.pwd_selector, seconds)
        self.click('xpath', loginpage.login_button_selector, seconds)








# El código aquí solo se ejecuta si este archivo es ejecutado directamente
if __name__ == "__main__":
    # Cambia entre "chrome" y "firefox" según el navegador que quieras usar
    t=.7
    BARBAS = "https://practicetestautomation.com/practice-test-login/"
    browser = BrowserManager("chrome")
    browser.open_browser(BARBAS)
    input_username = browser.select_element('xpath', '//*[@id="username"]', t)
    input_username.send_keys("student")
    time.sleep(.6)
    input_pwd = browser.select_element('css', '#password', t)
    input_pwd.send_keys("Password1234")
    time.sleep(.6)
    time.sleep(2)
    browser.close_browser()