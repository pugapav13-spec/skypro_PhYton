import allure
from ui_pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class MainPage(BasePage):
    """
    Методы главной страницы сайта "Читай-город"
    "https://www.chitai-gorod.ru/", наследуются от BasePage:
    - Переход на главную страницу сайта,
    - Поиск по фразе в строке поиска
    """

    def init(self, driver: WebDriver):
        # Вызов конструктора BasePage
        super().__init__(driver)

    @allure.step("Перейти на главную страницу сайта.")
    def go_base_url(self):
        """
        Функция для перехода на главную страницу сайта.
        """
        self.go_to_url(self.base_url)

    @allure.step("Выполнить поиск фразы '{search_phrase}'")
    def search_by_phrase(self, search_phrase: str) -> str:
        """
        Выполняет поиск по заданной фразе и возвращает текст
        с результатами поиска.
            search_phrase: str - фраза для поиска (тестовые данные
                                 из файла test_data.json)
            return: str - текст о результатах поиска
        """
        # переменные для запросов
        search_field_locator = (By.NAME, "search")
        search_button_locator = (By.CLASS_NAME, "search-form__icon-search")
        search_results_locator = (By.CLASS_NAME, "search-page")
        search_title_locator = (By.CLASS_NAME, "search-title")

        try:
            self.enter_text(search_field_locator, search_phrase)
            self.click_element(search_button_locator)
            self.wait_for_element_visibility(search_results_locator)
            response = self.find_element(search_title_locator)
            return response.text
        except Exception:
            raise
