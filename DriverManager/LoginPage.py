import json
from DriverManager.Credentials import Credentials

class LoginPage:
    """
    Clase que representa una página de inicio de sesión.

    Contiene la URL de la página y los selectores para los campos de usuario, contraseña y el botón de login.
    """
    def __init__(self, id, url, username_selector, pwd_selector, login_button_selector, credentials):
        """
        Inicializa los detalles de la página de inicio de sesión.

        :param id: Nombre identificador de la página.
        :param url: La URL de la página de login.
        :param username_selector: Selector para el campo de nombre de usuario.
        :param pwd_selector: Selector para el campo de contraseña.
        :param login_button_selector: Selector para el botón de login.
        :param credentials: Objeto que contiene el nombre de usuario y la contraseña.

        :type id: str
        :type url: str
        :type username_selector: str
        :type pwd_selector: str
        :type login_button_selector: str
        :type credentials: Credentials
        """
        self.id = id
        self.url = url
        self.username_selector = username_selector
        self.pwd_selector = pwd_selector
        self.login_button_selector = login_button_selector
        self.credentials = credentials

    @staticmethod
    def read_login_data_from_json():
        """
        Lee los datos de 'DriverManager/data_load/login_data.json' y crea una lista de objetos LoginPage.

        La estructura del archivo JSON se explica en 'DriverManager/data_load/README.md'.

        :return: Una lista de objetos LoginPage.
        """
        data = json.load(open(r'data_load/login_data.json'))
        login_pages = []
        for entry in data:
            credentials = Credentials(entry['credentials']['username'], entry['credentials']['password'])
            login_page = LoginPage(
                entry['id'],
                entry['url'],
                entry['username_selector'],
                entry['password_selector'],
                entry['login_button_selector'],
                credentials
            )
            login_pages.append(login_page)
        return login_pages

    @staticmethod
    def get_login_page_by_id(page_id):
        """
        Devuelve un objeto LoginPage de la lista creada por LoginPage.read_login_data_from_json()
        si el 'id' coincide con el valor de 'page_id' proporcionado.
        Si no se encuentra devuelve None.

        :param page_id: 'id' del LoginPage buscado.

        :type page_id: str

        :return: El objeto LoginPage con el 'id' requerido, o None si no se encuentra.
        """
        for page in LoginPage.read_login_data_from_json():
            if page.id == page_id:
                return page
        return None

