import allure
from ui_pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException


class CartPage(BasePage):
    """
    Методы страницы работы с корзиной:
    - Переход в корзину,
    - Проверка наличия товара в корзине
    """

    def init(self, driver: WebDriver):
        # Вызов конструктора BasePage
        super().__init__(driver)

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """
        Переходит в корзину.
        """
        self.go_to_url(self.cart_url)

    @allure.step("Сверить наличие товара {product_name} в корзине.")
    def check_product_in_cart(self, product_name: str) -> bool:
        """
        Проверяет, что товар отображается в корзине.
        """
        try:
            locator = (By.CLASS_NAME, "product-cart-title__head")
            self.wait_for_element_visibility(locator)
            list_cart = self.driver.find_elements(*locator)
            for product in list_cart:
                if product.text == product_name:
                    return True

            return False
        except TimeoutException:
            return False
        except Exception:
            return False
