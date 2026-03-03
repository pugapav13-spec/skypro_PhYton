import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
from api.client import ApiClient

# Токен авторизации
BEARER_TOKEN = "Вставить токен"


@pytest.fixture(scope="session")
def api_client():
    """Фикстура API-клиента с Bearer токеном"""
    session = requests.Session()

    session.headers.update({
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
    })

    print("\n API-клиент создан с Bearer токеном")
    return ApiClient(session=session)


@pytest.fixture(scope="function")
def driver():
    """Фикстура веб-драйвера для UI-тестов"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    yield driver
    driver.quit()
