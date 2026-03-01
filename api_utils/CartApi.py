import requests
import allure


class CartApi:
    """
    Класс с методами для API-запросов при работе с корзиной товаров.
    - Поиск товара на главной странице сайта.
    - Очистка корзины товаров,
    - Получение кратких данных о составе корзины,
    - Получение информации о содержимом корзины,
    - Добавление товара в корзину по артикулу (id)б
    - Удаление товара из корзины по id.
    """
    @allure.step("""CartApi. URL:{cart_url}, {cart_short_url},
                 параметры для авторизации: {params}""")
    def __init__(self, cart_url: str, cart_short_url: str,
                 params: dict) -> None:
        """
        Инициализация метода 'CartApi'.
        Определяет сущность класса 'CartApi' и формирует
        параметры для requests-запросов:
        cart_url: str - основной URL для работы с корзиной,
        cart_short_url: str - URL для получения краткой информации
                        о содержимом корзины,
        params: dict - словарь с необходимыми для авторизации данными,
                        содержит ключи:
                        - token: str,
                        - user_agent: str,
                        - content_type: str.
        """
        self.cart_url = cart_url
        self.cart_short_url = cart_short_url
        self.params = params

    @allure.step("Очистить корзину товаров")
    def cart_delete_all(self) -> dict:
        path = self.cart_url
        resp = requests.delete(path, headers=self.params)
        return resp

    @allure.step("Получить краткие данные о составе корзины")
    def cart_short(self) -> dict:
        path = self.cart_short_url
        resp = requests.get(path, headers=self.params)
        return resp

    @allure.step("Получить полную информацию о содержимом корзины")
    def cart_info(self) -> dict:
        path = self.cart_url
        resp = requests.get(path, headers=self.params)
        return resp

    @allure.step("Добавить в корзину товар по артикулу: {add_id}.")
    def add_to_cart(self, add_id: dict) -> dict:
        path = self.cart_url + "/product"
        resp = requests.post(path, headers=self.params, json=add_id)
        return resp

    @allure.step("Удалить из корзины товар по id: {del_id}.")
    def del_from_cart(self, del_id: str) -> dict:
        path = self.cart_url + "/product/" + del_id
        resp = requests.delete(path, headers=self.params)
        return resp

    @allure.step("Изменить количество единиц товара: {quantity_id}.")
    def change_product_quantity(self, quantity_id: dict) -> dict:
        path = self.cart_url
        resp = requests.put(path, headers=self.params, json=quantity_id)
        return resp
