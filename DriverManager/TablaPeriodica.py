import os
import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from DriverManager.BrowserManager import BrowserManager
from DriverManager.LoginPage import LoginPage


class TablaPeriodica(BrowserManager):
    def __init__(self, browser_type):
        """
        Inicializa el driver basado en el navegador seleccionado.
        Inicializa sus atributos creando un LoginPage.

        :param browser_type: Tipo de navegador a usar. Acepta "chrome" y "firefox".

        :type browser_type: str

        :raises ValueError: Si el tipo de navegador no es soportado.
        """
        super().__init__(browser_type)
        self.loginpage = LoginPage.get_login_page_by_id('TABLA_P')

    def open_browser(self):
        """
        Abre la URL de login en CST y maximiza la ventana del navegador.
        """
        self.driver.get(self.loginpage.url)
        self.driver.maximize_window()



if __name__ == "__main__":
    # Cambia entre "chrome" y "firefox" según el navegador que quieras usar
    t=.7
    tp = TablaPeriodica("chrome")
    tp.open_browser()
    tp.select_element('id', 'Gases', t)
    time.sleep(2)
    o2_neutrones = tp.get_cell('Cloro', -2, t)




    print('*********************************')
    print(o2_neutrones.get_attribute('outerHTML'))
    print('*********************************')
    time.sleep(2)
    tp.close_browser()