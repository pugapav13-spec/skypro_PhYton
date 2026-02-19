import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List


class CartPage:
    """
    Page Object для страницы корзины интернет-магазина.
    Содержит методы для проверки содержимого корзины и оформления заказа.
    """
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы корзины.
        
        Args:
            driver: WebDriver экземпляр браузера
        """
        self.driver = driver
        self._cart_items = (By.CSS_SELECTOR, ".cart_item")
        self._item_names = (By.CSS_SELECTOR, ".inventory_item_name")
        self._checkout_button = (By.ID, "checkout")
    
    @allure.step("Получение списка товаров в корзине")
    def get_cart_items(self) -> List[str]:
        """
        Получает список названий товаров в корзине.
        
        Returns:
            List[str]: Список названий товаров в корзине
        """
        items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self._cart_items)
        )
        
        cart_items_names = []
        for item in items:
            item_name = item.find_element(*self._item_names).text
            cart_items_names.append(item_name)
        
        allure.attach(
            f"Товары в корзине: {', '.join(cart_items_names)}",
            name="Содержимое корзины",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return cart_items_names
    
    @allure.step("Переход к оформлению заказа")
    def click_checkout(self) -> None:
        """
        Нажимает кнопку Checkout для оформления заказа.
        
        Returns:
            None
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._checkout_button)
        ).click()
        allure.attach(
            "Нажата кнопка оформления заказа",
            name="Действие",
            attachment_type=allure.attachment_type.TEXT
        )
