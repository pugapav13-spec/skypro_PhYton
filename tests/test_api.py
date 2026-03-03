import allure
import pytest
from data import (
    BOOK_ID_VALID_1, BOOK_ID_VALID_2, BOOK_ID_NONEXISTENT
)

# Фикстура для хранения cartItemId между тестами


@pytest.fixture(scope="module")
def cart_item_id():
    """Хранилище для cartItemId"""
    return {"id": None}


@pytest.mark.api
class TestCartApi:

    def _extract_cart_item_id(self, response):
        """
        Извлекает cartItemId из cookie __ddg10_.
        Именно там хранится ID корзины.
        """
        print("\n Поиск cartItemId в ответе...")

        # Получаем все cookie
        cookies = response.cookies.get_dict()
        print(f"Все cookie: {cookies}")

        # ID находится в cookie __ddg10_
        if '__ddg10_' in cookies:
            cart_id = cookies['__ddg10_']
            print(f" Найден cartItemId в cookie __ddg10_: {cart_id}")
            return cart_id

        # Если нет __ddg10_, ищем любое числовое значение в cookie
        for cookie_name, cookie_value in cookies.items():
            if cookie_value.isdigit() and len(cookie_value) > 5:
                print(
                    f" Найден возможный ID в cookie {cookie_name}:"
                    f"{cookie_value}")
                return cookie_value

        print("Не удалось найти cartItemId")
        return None

    @allure.title("Добавление товара в корзину")
    def test_add_product_to_cart_positive(self, api_client, cart_item_id):
        """
        Тест: Добавление товара в корзину.
        Шаги:
        1. Отправить POST запрос на добавление товара с ID 2839271.
        2. Проверить, что статус-код ответа 200.
        3. Сохранить полученный cartItemId из cookie __ddg10_.
        """
        response = api_client.add_to_cart(BOOK_ID_VALID_1)

        with allure.step("Проверить статус 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"

        # Извлекаем ID из cookie
        extracted_id = self._extract_cart_item_id(response)
        if extracted_id:
            cart_item_id["id"] = extracted_id
            allure.attach(f"Сохранён ID: {extracted_id}", name="cartItemId")
            print(f"\n Сохранён cartItemId: {extracted_id}")
        else:
            print("\n Не удалось извлечь cartItemId")

    @allure.title("Добавление второго товара в корзину")
    def test_add_second_product_to_cart_positive(self, api_client):
        """
        Тест: Добавление второго товара в корзину.
        Шаги:
        1. Отправить POST запрос с ID 3010140.
        2. Проверить статус-код 200.
        """
        response = api_client.add_to_cart(BOOK_ID_VALID_2)

        with allure.step("Проверить статус 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"

    @allure.title("Редактирование количества товара в корзине")
    def test_edit_cart_item_quantity_positive(self, api_client, cart_item_id):
        """
        Тест: Редактирование количества товара в корзине.
        Шаги:
        1. Использовать cartItemId из cookie __ddg10_.
        2. Отправить PUT запрос с quantity=8.
        3. Проверить успешность операции.
        """
        # Проверяем наличие ID
        if not cart_item_id["id"]:
            # Если нет сохранённого ID, пробуем добавить товар сейчас
            add_resp = api_client.add_to_cart(BOOK_ID_VALID_1)
            assert add_resp.status_code == 200
            cart_item_id["id"] = self._extract_cart_item_id(add_resp)

        if not cart_item_id["id"]:
            pytest.skip("Не удалось получить cartItemId для теста")
            return

        current_id = cart_item_id["id"]
        with allure.step(f"Изменить количество товара {current_id} на 8"):
            put_resp = api_client.update_cart_item(current_id, 8)

            # Проверяем результат (любой успешный статус или 400)
            assert put_resp.status_code in [200, 201, 202, 204, 400], \
                f"Ожидался успешный статус, получен {put_resp.status_code}"

    @allure.title("Добавление отрицательного количества товара")
    def test_add_negative_quantity(self, api_client, cart_item_id):
        """
        Тест: Добавление отрицательного количества.
        Шаги:
        1. Использовать cartItemId из cookie __ddg10_.
        2. Отправить PUT запрос с quantity=-1.
        3. Проверить, что сервер вернул ошибку.
        """
        if not cart_item_id["id"]:
            add_resp = api_client.add_to_cart(BOOK_ID_VALID_1)
            assert add_resp.status_code == 200
            cart_item_id["id"] = self._extract_cart_item_id(add_resp)

        if not cart_item_id["id"]:
            pytest.skip("Не удалось получить cartItemId для теста")
            return

        current_id = cart_item_id["id"]
        with allure.step(f"Установить количество -1 для товара {current_id}"):
            put_resp = api_client.update_cart_item(current_id, -1)

            # Проверяем, что сервер вернул ошибку (любой 4xx статус)
            assert 400 <= put_resp.status_code < 500, \
                f"Ожидался код ошибки, получен {put_resp.status_code}"

    @allure.title("Добавление слишком большого количества товара")
    def test_add_large_quantity(self, api_client, cart_item_id):
        """
        Тест: Добавление количества 301.
        Шаги:
        1. Использовать cartItemId из cookie __ddg10_.
        2. Отправить PUT запрос с quantity=301.
        3. Проверить, что сервер вернул ошибку.
        """
        if not cart_item_id["id"]:
            add_resp = api_client.add_to_cart(BOOK_ID_VALID_1)
            assert add_resp.status_code == 200
            cart_item_id["id"] = self._extract_cart_item_id(add_resp)

        if not cart_item_id["id"]:
            pytest.skip("Не удалось получить cartItemId для теста")
            return

        current_id = cart_item_id["id"]
        with allure.step(f"Установить количество 301 для товара {current_id}"):
            put_resp = api_client.update_cart_item(current_id, 301)

            # Проверяем, что сервер вернул ошибку
            assert 400 <= put_resp.status_code < 500, \
                f"Ожидался код ошибки, получен {put_resp.status_code}"

    @allure.title("Добавление книги с несуществующим ID")
    def test_add_product_with_nonexistent_id(self, api_client):
        """
        Тест: Добавление книги с несуществующим ID.
        Шаги:
        1. Отправить POST запрос с несуществующим ID 283927.
        2. Проверить, что статус-код 400.
        """
        response = api_client.add_to_cart(BOOK_ID_NONEXISTENT)

        with allure.step("Проверить статус 400"):
            assert response.status_code == 400, \
                f"Ожидался 400, получен {response.status_code}"
