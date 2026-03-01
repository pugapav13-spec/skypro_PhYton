import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from api_utils.CartApi import CartApi
from api_utils.BaseApi import BaseApi
from api_utils.SearchApi import SearchApi
from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider


@pytest.fixture(scope="session")
def browser():
    with allure.step("Открыть и настроить браузер"):
        timeout = ConfigProvider().getint("ui", "timeout")
        browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()))
        browser.implicitly_wait(timeout)
        browser.maximize_window()
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()


@pytest.fixture
@allure.step("Создание базовых настроек для работы API-методов")
def api_base() -> BaseApi:
    base_url = (ConfigProvider().get("api", "base_url"))
    track_url = (ConfigProvider().get("api", "base_url") +
                 ConfigProvider().get("api", "track"))
    token = DataProvider().get_token()
    user_agent = DataProvider().get_user_agent()
    content_type = DataProvider().get_content_type()
    params = {
        'Authorization': token,
        'user-agent': user_agent,
        'Content-Type': content_type
    }
    api_base = BaseApi(base_url, track_url, params)
    return api_base


@pytest.fixture
@allure.step("Создание настроек для работы с корзиной (CartApi)")
def api_cart() -> CartApi:
    cart_url = (ConfigProvider().get("api", "base_url") +
                ConfigProvider().get("api", "cart"))
    cart_short_url = (ConfigProvider().get("api", "base_url") +
                      ConfigProvider().get("api", "cart_short"))
    token = DataProvider().get_token()
    user_agent = DataProvider().get_user_agent()
    content_type = DataProvider().get_content_type()
    params = {
        'Authorization': token,
        'user-agent': user_agent,
        'Content-Type': content_type
    }
    api_cart = CartApi(cart_url, cart_short_url, params)
    return api_cart


@pytest.fixture
@allure.step("Создание настроек для работы с поиском (SearchApi)")
def api_search() -> SearchApi:
    search_url = (ConfigProvider().get("api", "base_url") +
                  ConfigProvider().get("api", "search"))
    token = DataProvider().get_token()
    user_agent = DataProvider().get_user_agent()
    content_type = DataProvider().get_content_type()
    params = {
        'Authorization': token,
        'user-agent': user_agent,
        'Content-Type': content_type
    }
    api_search = SearchApi(search_url, params)
    return api_search


@pytest.fixture(scope="session")
@allure.step("Вычитывание данных для тестов из test_data")
def test_data():
    return DataProvider()


@pytest.fixture(params=DataProvider().get_list("search_phrase_positive"))
def search_positive(request):
    """
    Фикстура возвращает список с данными из test_data.json,
    по ключу 'search_phrase_positive'.
    """
    return request.param


@pytest.fixture(params=DataProvider().get_list("search_phrase_negative"))
def search_negative(request):
    """
    Фикстура возвращает список с данными из test_data.json,
    по ключу 'search_phrase_negative'.
    """
    return request.param


@pytest.fixture(params=DataProvider().get_list("number_phone_invalid"))
def number_phone_invalid(request):
    return request.param


@pytest.fixture
@allure.step("Получить данные о товаре для проведения тестов")
def inside_test_data() -> dict:
    """
    Фикстура формирует тестовые данные для использования в тестах.

    return -> dict - словарь с атрибутами произвольного товара.
    """
    for_data_url = (ConfigProvider().get("api", "base_url") +
                    ConfigProvider().get("api", "for_data"))
    token = DataProvider().get_token()
    user_agent = DataProvider().get_user_agent()
    params = {
        'Authorization': token,
        'user-agent': user_agent
    }
    path = for_data_url
    resp = requests.get(path, headers=params)
    dict = resp.json()["data"][0]["attributes"]
    return dict
