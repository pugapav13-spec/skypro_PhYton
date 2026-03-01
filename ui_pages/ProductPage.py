import allure
from ui_pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException


class ProductPage(BasePage):
    """
    Методы страницы карточки товара
    """

    def init(self, driver: WebDriver):
        # Вызов конструктора BasePage
        super().__init__(driver)

    @allure.step("Покупка товара (клик на кнопку 'Купить')")
    def buy_product(self) -> None:
        """
        Метод выполняет имитацию клика по кнопке 'Купить'
        после ожидания ее доступности к нажатию.
            locator: tuple - локатор для элемента вида (By.ID, "element_id")
            return: None
        """
        try:
            locator = (By.CLASS_NAME, "product-offer-button")
            element = self.wait_for_element_clickable(locator)
            element.click()
        except TimeoutException:
            raise TimeoutException(
                "Не удалось дождаться кликабельности кнопки 'Купить'")
        except Exception as e:
            raise Exception(f"Ошибка при клике на кнопку 'Купить': {e}")
