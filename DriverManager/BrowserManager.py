import os
import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from DriverManager.LoginPage import LoginPage
from selenium.webdriver.remote.webelement import WebElement



class BrowserManager():
    def __init__(self, browser_type):
        """
        Inicializa el driver basado en el navegador seleccionado.

        :param browser_type: Tipo de navegador a usar. Acepta "chrome" y "firefox".

        :type browser_type: str

        :raises ValueError: Si el tipo de navegador no es soportado.
        """
        # Rutas dinámicas para los webdrivers
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene directorio actual del archivo que lo ejecuta
        chrome_driver_path = os.path.join(base_dir, "webdrivers", "chromedriver.exe")  # Construyte la ruta absoluta
        gecko_driver_path = os.path.join(base_dir, "webdrivers", "geckodriver.exe")  # Construyte la ruta absoluta

        # Diccionario para mapear el navegador con el servicio y el driver correspondiente
        browser_mapping = {
            'chrome': (ChromeService, webdriver.Chrome, chrome_driver_path),
            'firefox': (FirefoxService, webdriver.Firefox, gecko_driver_path)
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
        Selecciona un elemento en la página web utilizando diferentes tipos de selectores predefinidos.

        Espera a que el elemento sea visible y lo desplaza a la vista.

        :param selector_type: Acepta los valores 'xpath', 'id', 'css', 'name' y 'link'.
        :param selector: El valor del selector, como la expresión XPath o css, el id, el valor del atributo name, o texto parcial de un link.
        :param seconds: Segundos antes de pasar a la siguiente tarea.

        :type selector_type: str
        :type selector: str
        :type seconds: float

        :return: El WebElement seleccionado si se encuentra. Retorna None si no se encuentra el elemento.
        :rtype: WebElement or None

        :raises TimeoutException: Si no se encuentra el elemento en el tiempo permitido, reintentará encontrarlo hasta 'retry_count' veces.
        :raises NoSuchElementException: Si el elemento no se encuentra en el DOM.
        :raises StaleElementReferenceException: Si el elemento ya no es un referente válido en el DOM.
        """
        # Se definen opciones fijas para el tipo de selector
        by_mapping = {
            'xpath': By.XPATH,
            'id': By.ID,
            'css': By.CSS_SELECTOR,
            'name': By.NAME,
            'link': By.PARTIAL_LINK_TEXT
        }
        # Comprueba que el tipo de selector está contemplado para esta función
        if selector_type not in by_mapping:
            print(f"Error: Tipo de selector '{selector_type}' no es válido.")
            return None

        attempt = 0  # intentos
        retry_count = 2  # contador de reintentos
        while attempt < retry_count:
            try:
                # Espera explícita hasta que el elemento sea visible
                element = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((by_mapping[selector_type], selector))
                )
                # Scroll hasta el elemento
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                # Espera el tiempo especificado
                time.sleep(seconds)
                return element

            except TimeoutException:
                # Reintenta localizar el elemento hasta 'retry_count' veces antes de devolver None
                attempt += 1
                if attempt == retry_count:
                    print(
                        f"\n\t*** = ***\nTimeout: No se pudo encontrar el elemento con selector: {selector} tras {retry_count} intentos.")
                    return None

            except NoSuchElementException:
                print(f"\n\t*** = ***\nError: El elemento con selector: {selector} no fue encontrado en el DOM.")
                return None

            except StaleElementReferenceException:
                print(f"\n\t*** = ***\nError: El elemento con selector: {selector} ya no es un referente válido en el DOM.")
                return None

    def select_all_elements(self, selector_type, selector):
        """
        Encuentra y devuelve todos los elementos que coincidan con el XPath dado.

        :param selector_type: Acepta los valores 'xpath', 'css' y 'tag'.
        :param selector: El valor del selector, como la expresión XPath o css o el tag_name. ("h1")

        :type selector_type: str
        :type selector: str

        :return: Lista de WebElement si se encuentran, o una lista vacía [] si no se encuentran.
        :rtype: list[WebElement]

        :raises TimeoutException: Si no se encuentran elementos en el tiempo permitido, reintentará encontrarlos hasta 'retry_count' veces.
        :raises NoSuchElementException: Si los elementos no se encuentra en el DOM.
        :raises StaleElementReferenceException: Si el XPath ya no es un referente válido en el DOM.
        """
        # Se definen opciones fijas para el tipo de selector
        by_mapping = {
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'tag': By.TAG_NAME
        }
        # Comprueba que el tipo de selector está contemplado para esta función
        if selector_type not in by_mapping:
            print(f"\n\t*** = ***\nError: Tipo de selector '{selector_type}' no es válido.")
            return None

        attempt = 0  # intentos
        retry_count = 2  # contador de reintentos
        while attempt < retry_count:
            try:
                # Espera explícita hasta que los elemento sea visible
                list_of_elements = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((by_mapping[selector_type], selector))
                )
                # for element in list_of_elements:
                #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                return list_of_elements

            except TimeoutException:
                # Reintenta localizar el elemento hasta 'retry_count' veces antes de devolver None
                attempt += 1
                if attempt == retry_count:
                    print(
                        f"\n\t*** = ***\nTimeout: No se pudieron encontrar los elementos con {selector_type} {selector} tras {retry_count} intentos.")
                    return []

            except NoSuchElementException:
                print(f"\n\t*** = ***\nError: No se han encontrado elementos con {selector_type} {selector} no fue encontrado en el DOM.")
                return []

            except StaleElementReferenceException:
                print(f"\n\t*** = ***\nError: {selector_type} {selector} ya no es un referente válido en el DOM.")
                return []

    def select_element_by_text(self, text, seconds):
        """
        Genera un xpath que contiene 'text' y llama a select_element() con los argumentos
        By.XPATH y el xpath generado.

        Selecciona el primer elemento que encuentra que contiene el texto especificado.

        Espera a que el elemento sea visible y lo desplaza a la vista.

        :param text: El texto que debe contener el elemento que se está buscando.
        :param seconds: Tiempo en segundos a esperar entre acciones.

        :type text: str
        :type seconds: float

        :return: El WebElement seleccionado si se encuentra. Retorna None si no se encuentra.
        :rtype: WebElement or None
        """
        xpath = f"//*[contains(text(), '{text}')]"
        return self.select_element('xpath', xpath, seconds)

    def get_xpath_of_element(self, element):
        """
        Devuelve el XPath de un elemento dado en una página web.

        :param element: El WebElement del cual obtener el XPath.

        :type element: WebElement

        :return: Una cadena con el XPath del elemento.

        :rtype: str
        """
        return self.driver.execute_script("""
            function getElementXPath(element) {
                if (element.id !== '') {
                    // Si el elemento tiene un id, se usa el id en el XPath
                    return '//*[@id="' + element.id + '"]';
                }
                if (element === document.body) {
                    // Si el elemento es el body, se retorna el XPath correspondiente
                    return '/html/body';
                }

                var ix = 0;
                var siblings = element.parentNode.childNodes;
                for (var i = 0; i < siblings.length; i++) {
                    var sibling = siblings[i];
                    if (sibling === element) {
                        // Devuelve el XPath con el índice basado en los hermanos
                        return getElementXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                    }
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                        ix++;
                    }
                }
            }
            return getElementXPath(arguments[0]);
        """, element)

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

    def get_row_by_text(self, text, seconds):
        """
        Busca un <tr> que contiene un <td> o <th> que contiene el texto proporcionado, ya sea directamente o en sus descendientes.

        :param text: El texto a buscar dentro de las celdas (td o th).
        :param seconds: Tiempo en segundos a esperar entre acciones.

        :type text: str
        :type seconds: float

        :return: El WebElement correspondiente al <tr> que contiene el texto.
        :rtype: WebElement
        """
        # Construir un XPath que busque un <tr> que tenga un <td> o <th> donde el texto esté presente
        xpath = f"//tr[td[contains(text(), '{text}') or .//*[contains(text(), '{text}')]] or th[contains(text(), '{text}') or .//*[contains(text(), '{text}')]]]"

        # Usar la función select_element con ese XPath
        row_element = self.select_element('xpath', xpath, seconds)

        return row_element

    def get_row_children(self, text, seconds):
        """
        Obtiene todos los <td> o <th> de la fila que contiene el texto proporcionado.

        :param text: El texto a buscar dentro de las celdas (td o th).
        :param seconds: Tiempo en segundos a esperar entre acciones.

        :type text: str
        :type seconds: float

        :return: Lista de WebElement correspondientes a las celdas (td o th) en la fila.
        :rtype: list[WebElement]
        """
        fila = self.get_row_by_text(text, seconds)
        xpath_fila = self.get_xpath_of_element(fila)
        xpath_children = f"{xpath_fila}/td | {xpath_fila}/th"  # Combina ambos tipos de celdas
        return self.select_all_elements('xpath', xpath_children)

    def _get_num_column(self, text_title, seconds):
        """
        Devuelve el número de la columna a la que pertenece 'text_title',
        siendo la de más a la izquierda la número 1.

        :param text_title: Texto representativo de la columna a buscar.
        :param seconds: Tiempo en segundos a esperar entre acciones.

        :type text_title: str
        :type seconds: float

        :return: El número de la columna al que pertenece el texto.
        :rtype: int
        """

        titles = self.get_row_children(text_title, seconds)
        n = 0
        for title in titles:
            n += 1
            if text_title in title.get_attribute('outerHTML'):
                return n
        return None


    def get_cell(self, text, column, seconds):
        """
        Obtiene el <td> o <th> de una fila específica que contiene el texto proporcionado en la columna indicada.

        :param text: El texto a buscar dentro de las celdas (td o th).
        :param column: El número de la columna de la celda que se quiere obtener (1-indexed) o el título de la columna buscada.
        :param seconds: Tiempo en segundos a esperar entre acciones.

        :type text: str
        :type column: int | str
        :type seconds: float

        :return: El WebElement correspondiente al <td> o <th> en la columna indicada, o None si no se encuentra.
        :rtype: WebElement
        """
        elements = self.get_row_children(text, seconds)
        # Determinar el número de columna basado en el tipo del argumento 'column'
        if isinstance(column, int):
            num_column = column
        elif isinstance(column, str):
            num_column = self._get_num_column(column, seconds)
            if num_column is None:  # Validar si el título de la columna no se encontró
                print(f"\n\t*** = ***\nError: No se encontró la columna con título '{column}'.")
                return None
        else:
            print("\n\t*** = ***\nEl tipo de valor 'column' no es válido.")
            return  None

        # Asegurar que la columna existe en la fila
        if len(elements) >= num_column > 0:
            return elements[num_column - 1]
        else:
            print(f"\n\t*** = ***\nError: La fila tiene de 1 a {len(elements)} columnas, pero se pidió la {num_column}.")
            return None


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