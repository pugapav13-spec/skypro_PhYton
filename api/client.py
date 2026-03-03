import allure
import requests
from config import API_BASE_URL, API_GATE_URL, \
    CART_PRODUCT_ENDPOINT, CART_ENDPOINT


class ApiClient:
    def __init__(self, session: requests.Session = None):
        self.session = session or requests.Session()
        self.base_url = API_BASE_URL
        self.gate_url = API_GATE_URL

    @allure.step("POST /cart/product – добавить товар в корзину")
    def add_to_cart(self, book_id: int):
        """Добавление товара в корзину"""
        url = f"{self.base_url}{CART_PRODUCT_ENDPOINT}"
        payload = {"id": book_id}
        print(f"\n Запрос: POST {url}")
        print(f" Тело: {payload}")
        response = self.session.post(url, json=payload)
        print(f" Статус: {response.status_code}")
        return response

    @allure.step("PUT /cart – изменить количество товара")
    def update_cart_item(self, cart_item_id: int, quantity: int):
        """Изменение количества товара в корзине"""
        url = f"{self.gate_url}{CART_ENDPOINT}"
        item_id = int(cart_item_id) if cart_item_id else 0
        payload = [{"id": item_id, "quantity": quantity}]
        print(f"\n Запрос: PUT {url}")
        print(f" Тело: {payload}")
        response = self.session.put(url, json=payload)
        print(f" Статус: {response.status_code}")
        return response

    @allure.title("DELETE /cart/product – удалить товар из корзины")
    def delete_cart_item(self, cart_item_id: int):
        """Удаление товара из корзины"""
        url = f"{self.gate_url}{CART_ENDPOINT}/product/{cart_item_id}"
        print(f"\n Запрос: DELETE {url}")
        response = self.session.delete(url)
        print(f" Статус: {response.status_code}")
        return response
