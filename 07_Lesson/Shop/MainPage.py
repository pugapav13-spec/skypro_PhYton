from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self._driver = driver
        self._driver.implicitly_wait(4)

    def add_products(self, products_to_add=None):
        wait = WebDriverWait(self._driver, 10)
        wait.until(EC.presence_of_element_located
                   ((By.CLASS_NAME, "inventory_list"))
        )

        if products_to_add is None:
            products_to_add = [
                "Sauce Labs Backpack",
                "Sauce Labs Bolt T-Shirt",
                "Sauce Labs Onesie"
            ]
        elif isinstance(products_to_add, str):
            products_to_add = [products_to_add]

        added_products = []

        for product_name in products_to_add:
            add_button = self._driver.find_element(
                By.XPATH,
                f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button"
            )
            add_button.click()
            added_products.append(product_name)
        return added_products

    def go_to_cart(self):
        cart_icon = self._driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
