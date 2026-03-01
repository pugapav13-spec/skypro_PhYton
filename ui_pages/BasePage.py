import allure
from configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """
    Общие методы для PageObject:
    - Переход на заданную страницу сайта,
    - Получение текущего URL,
    - Ожидание видимости элемента,
    - Ожидание кликабельности элемента,
    - Ввод текста в элемент,
    - Клик на элемент,
    - Доступность элемента,
    - Поиск элемента,
    - Получение значения атрибута элемента
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.base_url = ConfigProvider().get("ui", "base_url")
        self.waiting = ConfigProvider().get("ui", "wait_driver")
        self.cart_path = ConfigProvider().get("ui", "cart")
        self.cart_url = self.base_url + self.cart_path

    @allure.step("Перейти на страницу: {any_url}.")
    def go_to_url(self, any_url: str) -> None:
        """
        Общая функция для перехода на заданную страницу сайта.
            any_url: str - адрес нужной страницы сайта
            return: None
        """
        self.driver.get(any_url)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """
        Общая функция для получения текущего URL
        """
        return self.driver.current_url

    @allure.step("Ожидание кликабельности элемента: '{locator}'")
    def wait_for_element_clickable(self, locator: tuple):
        """
        Общая функция для ожидания кликабельности элемента.
            locator: tuple - локатор для поля (например, (By.ID, "element_id"))
        В случае ошибки, выбрасывается исключение TimeoutException.
        """
        try:
            element = WebDriverWait(self.driver, self.waiting).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Элемент {locator} не доступен\
        для клика после {self.waiting} секунд ожидания")
        except NoSuchElementException:
            raise TimeoutException(
                f"Элемент '{locator}' не найден на странице.")
        except Exception as e:
            raise Exception(f"Непредвиденная ошибка при ожидании\
                             кликабельности элемента '{locator}': {e}")

    @allure.step("Ожидание видимости элемента: '{locator}'")
    def wait_for_element_visibility(self, locator: tuple):
        """
        Общая функция для ожидания видимости элемента.
            locator: tuple - локатор для поля вида (By.ID, "element_id")
        В случае ошибки, выбрасывается исключение TimeoutException.
        """
        try:
            element = WebDriverWait(self.driver, self.waiting).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Элемент {locator} не виден\
        после {self.waiting} секунд ожидания")
        except NoSuchElementException:
            raise TimeoutException(
                f"Элемент '{locator}' не найден на странице.")
        except Exception as e:
            raise Exception(f"Непредвиденная ошибка при ожидании\
                             видимости элемента '{locator}': {e}")

    @allure.step("Ввести текст: '{text}' в элемент: '{locator}'")
    def enter_text(self, locator: tuple, text: str) -> None:
        """
        Общая функция для ввода текста в заданный элемент.
            locator: tuple - локатор для поля вида (By.ID, "element_id")
            text: str - текст для ввода в поле
            return: None
        """
        element = self.wait_for_element_clickable(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Ожидание и клик на элементе: '{locator}'")
    def click_element(self, locator: tuple) -> None:
        """
        Общая функция для клика на элемент.
        Метод выполняет имитацию клика после ожидания
        доступности элемента к нажатию.
            locator: tuple - локатор для элемента вида (By.ID, "element_id")
            return: None
        """
        element = self.wait_for_element_clickable(locator)
        element.click()

    @allure.step("Поиск элемента: '{locator}'")
    def find_element(self, locator: tuple):
        """
        Общая функция для поиска элемента.
            locator: tuple - локатор для элемента вида (By.ID, "element_id")
        В случае если элемент не найден, выбрасывается исключение
         TimeoutException
        """
        try:
            element = WebDriverWait(self.driver, self.waiting).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Превышено время ожидания {self.waiting}")

    @allure.step("Определить доступность элемента по атрибуту: '{locator}'")
    def element_disabled(self, locator: str):
        """
        Общая функция для определения доступности элемента.
            locator: tuple - локатор для элемента вида (By.ID, "element_id")
        В случае ошибки, выбрасывается исключение TimeoutException.
        """
        try:
            element = WebDriverWait(self.driver, self.waiting).until(
                EC.element_attribute_to_include(locator, "disabled")
            )
            return element
        except TimeoutException:
            return None
        except Exception as e:
            raise Exception(f"Произошла непредвиденная ошибка: {e}")

    @allure.step("Получить значение атрибута элемента: '{attribute}'")
    def get_element_attribute(self, locator: str, attribute: str):
        """
        Общая функция для получения значения указанного атрибута.
            locator: tuple - локатор для элемента вида (By.ID, "element_id")
            attribute: str - атрибут для поиска
            return: str | None - найденное значение атрибута или ничего.
        В случае ошибки, выбрасывается исключение Exception.
        """
        try:
            element = WebDriverWait(self.driver, self.waiting).until(
                EC.presence_of_element_located(locator)
            )
            attribute_value = element.get_attribute(attribute)
            return attribute_value
        except Exception as e:
            raise Exception(f"Произошла ошибка: {e}")
