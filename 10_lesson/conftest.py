import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser() -> webdriver.Chrome:
    """
    Фикстура для создания Chrome браузера.
    
    Returns:
        webdriver.Chrome: Экземпляр Chrome WebDriver
        
    Yields:
        webdriver.Chrome: Экземпляр драйвера для использования в тесте
        
    После завершения теста автоматически закрывает браузер.
    """
    with allure.step("Инициализация Chrome браузера"):
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
        driver.implicitly_wait(10)
        driver.maximize_window()
        allure.attach(
            "Chrome браузер успешно запущен", 
            name="Информация", 
            attachment_type=allure.attachment_type.TEXT
        )
    
    yield driver
    
    with allure.step("Закрытие Chrome браузера"):
        driver.quit()


@pytest.fixture
def firefox_driver() -> webdriver.Firefox:
    """
    Фикстура для создания Firefox браузера.
    
    Returns:
        webdriver.Firefox: Экземпляр Firefox WebDriver
        
    Yields:
        webdriver.Firefox: Экземпляр драйвера для использования в тесте
        
    После завершения теста автоматически закрывает браузер.
    """
    with allure.step("Инициализация Firefox браузера"):
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install())
        )
        driver.implicitly_wait(10)
        driver.maximize_window()
        allure.attach(
            "Firefox браузер успешно запущен", 
            name="Информация", 
            attachment_type=allure.attachment_type.TEXT
        )
    
    yield driver
    
    with allure.step("Закрытие Firefox браузера"):
        driver.quit()
