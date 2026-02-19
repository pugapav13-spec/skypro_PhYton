import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List


class MainPage:
    """
    Page Object для главной страницы интернет-магазина.
    Содержит методы для работы с каталогом товаров и корзиной.
    """
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация главной страницы.
        
        Args:
            driver: WebDriver экземпляр браузера
        """
        self.driver = driver
        self._add_buttons = (By.CSS_SELECTOR, ".btn_inventory")
        self._cart_link = (By.CSS_SELECTOR, ".shopping_cart_link")
        self._inventory_items = (By.CSS_SELECTOR, ".inventory_item")
        self._item_names = (By.CSS_SELECTOR, ".inventory_item_name")
    
    @allure.step("Добавление товаров в корзину")
    def add_products(self) -> List[str]:
        """
        Добавляет товары в корзину в следующем порядке:
        - Sauce Labs Backpack
        - Sauce Labs Bolt T-Shirt
        - Sauce Labs Onesie
        
        Returns:
            List[str]: Список названий добавленных товаров
        """
        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]
        added_products = []
        
        with allure.step("Поиск товаров в каталоге"):
            items = self.driver.find_elements(*self._inventory_items)
        
        for item in items:
            with allure.step("Проверка названия товара"):
                item_name = item.find_element(*self._item_names).text
                if item_name in products_to_add:
                    with allure.step(f"Добавление товара: {item_name}"):
                        add_button = item.find_element(*self._add_buttons)
                        add_button.click()
                        added_products.append(item_name)
                        allure.attach(
                            f"Добавлен товар: {item_name}",
                            name="Товар добавлен",
                            attachment_type=allure.attachment_type.TEXT
                        )
        
        allure.attach(
            f"Добавленные товары: {', '.join(added_products)}",
            name="Список добавленных товаров",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return added_products
    
    @allure.step("Переход в корзину")
    def go_to_cart(self) -> None:
        """
        Выполняет переход на страницу корзины.
        
        Returns:
            None
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._cart_link)
        ).click()
        allure.attach(
            "Переход в корзину выполнен",
            name="Навигация",
            attachment_type=allure.attachment_type.TEXT
        )
