import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():
    """Фикстура для Chrome браузера"""
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()


@pytest.fixture
def firefox_driver():
    """Фикстура для Firefox браузера"""
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install())
    )
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()
