import allure
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import UI_BASE_URL


class SearchPage:
    """Page Object для главной страницы и поиска"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    _search_input = (By.ID, "app-search")
    _search_button = (
        By.XPATH,
        "//button[@type='submit'"
        "and contains(@class, 'header-search__button')]"
    )
    _search_button_alt = (
        By.XPATH,
        "/html/body/div[2]/div/div[2]/div/div/header/"
        "div/div[1]/div/div/div[1]/form/button"
    )
    _results_summary = (
        By.XPATH,
        "//div[contains(text(),'Нашли') or contains(text(),'товар')]")
    _no_results_message = (
        By.XPATH, "//*[contains(text(),'Похоже, у нас такого нет')]")

    def open(self):
        """Открыть главную страницу"""
        with allure.step("Открыть главную страницу"):
            self.driver.get(UI_BASE_URL)
            try:
                cookie_accept = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(),'Принять')]"))
                )
                cookie_accept.click()
            except TimeoutException:
                pass

    def search(self, query: str):
        """Ввести запрос и выполнить поиск"""
        with allure.step(f"Ввести в поиск '{query}' и нажать кнопку"):
            input_field = self.wait.until(EC.element_to_be_clickable
                                          (self._search_input))
            input_field.clear()
            input_field.send_keys(query)

            try:
                search_btn = self.wait.until(EC.element_to_be_clickable
                                             (self._search_button))
            except TimeoutException:
                search_btn = self.wait.until(EC.element_to_be_clickable
                                             (self._search_button_alt))
            search_btn.click()

            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "body")))

    def get_results_count(self) -> int:
        """Получить количество найденных товаров"""
        with allure.step("Получить количество найденных товаров"):
            try:
                elem = self.wait.until(
                    EC.visibility_of_element_located(self._results_summary))
                text = elem.text
                match = re.search(r'(\d[\d\s]*\d|\d)', text)
                if match:
                    count_str = match.group(1).replace(' ', '')
                    return int(count_str)
            except TimeoutException:
                pass
            return 0

    def no_results_message_displayed(self) -> bool:
        """Проверить наличие сообщения об отсутствии результатов"""
        with allure.step("Проверить сообщение об отсутствии результатов"):
            try:
                self.wait.until(EC.visibility_of_element_located
                                (self._no_results_message))
                return True
            except TimeoutException:
                return False
