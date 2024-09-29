import json
import pytest
from DriverManager.BrowserManager import BrowserManager
from DriverManager.Credentials import Credentials
from DriverManager.LoginPage import LoginPage

t=.4
# Mapeo de navegadores
browser_mapping = ['chrome', 'firefox']
# Cargar los datos del login desde el archivo JSON
pages_mapping = [page.url for page in LoginPage.read_login_data_from_json()]

# @pytest.fixture(scope='function')
# def browser(request):
#     """Fixture para inicializar el navegador."""
#     browser_name = request.param  # El nombre del navegador se pasa como parámetro
#     browser_instance = BrowserManager(browser_name)
#     yield browser_instance  # Devuelve la instancia del navegador
#     browser_instance.close_browser()  # Se ejecuta al final de la prueba

# @pytest.mark.parametrize('browser, page', [(b, p) for b in browser_mapping for p in pages_mapping])
# def test_open_google(browser, page):
#
#     browser = BrowserManager(browser)
#     browser.open_browser(page)
#     browser.close_browser()

@pytest.fixture(scope='function')
def browser():
    """Fixture para inicializar el navegador."""
    browser = BrowserManager('chrome')
    yield browser  # Devuelve la instancia del navegador
    browser.close_browser()  # Se ejecuta al final de la prueba

@pytest.mark.parametrize('page', pages_mapping)
def test_open_google(browser, page):
    browser.open_browser(page)

@pytest.mark.parametrize('loginpage', LoginPage.read_login_data_from_json())
def test_login(browser, loginpage):
    browser.login(loginpage, t)


def test_login_page_by_id(browser):

    page_id = 'BARBAS'
    login_page = LoginPage.get_login_page_by_id(page_id)

    if login_page:
        browser.login(login_page, t)
    else:
        print(f"Página con id '{page_id}' no encontrada.")
