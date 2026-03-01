import pytest
import allure
from api_utils.CartApi import CartApi
from api_utils.SearchApi import SearchApi
from selenium.common.exceptions import NoSuchElementException


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Проверка API: Полная очистка корзины товаров")
@allure.description("""Проверка API для полной очистки корзины.
Тест добавляет товар в корзину, затем удаляет все товары и проверяет,
что корзина стала пустой.""")
@allure.feature("API: Корзина товаров")
@pytest.mark.api
def test_cart_clear(api_cart: CartApi, inside_test_data: dict) -> None:
    """
    Тест проверяет работу функционала полной очистки корзины товаров -
    имитация нажатия кнопки 'Очистить корзину'.
    Тест добавляет товар в корзину, затем удаляет все товары и проверяет,
    что корзина стала пустой.
    Параметры
        api_cart: CartApi - сущность для работы класса 'CartApi'
        inside_test_data: dict - тестовые данные для добавления
                                 тестового товара в корзину.
    """
    product_added_id = dict({'id': inside_test_data['id']})
    added = api_cart.add_to_cart(product_added_id)

    before = api_cart.cart_info()
    before_count = len(before.json()['products'])

    delete = api_cart.cart_delete_all()

    after = api_cart.cart_short()
    after_count = after.json()['data']['quantity']

    with allure.step("Проверки Status Code."):
        with allure.step("Запрос: добавление товара: Status Code = 200"):
            assert added.status_code == 200, f"""Ошибка при обработке
 запроса на добавление товара в корзину: {added.status_code}"""
        with allure.step("""Запрос: получение информации о корзине
 до удаления. Status Code = 200"""):
            assert before.status_code == 200, f"""Ошибка при обработке
 запроса на получение информации о корзине до удаления: {before.status_code}"""
        with allure.step("Проверка: количество товаров до удаления > 0"):
            assert before_count > 0, "Перед удалением корзина пуста."
        with allure.step("""Запрос: удаление товара из корзины.
 Status Code = 204"""):
            assert delete.status_code == 204, f"""Ошибка при обработке
 запроса на удаление товара из корзины: {delete.status_code}"""
        with allure.step("""Запрос: получение информации о корзине
 после удаления. Status Code = 200"""):
            assert after.status_code == 200, f"""Ошибка при обработке запроса
 на получение информации о корзине после удаления: {delete.status_code}"""
    with allure.step("Проверка: количество товаров после удаления =0"):
        assert after_count == 0, "После удаления корзина не пуста"


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Проверка API: Добавление товара в корзину")
@allure.description("""Проверка API для добавления товара в корзину.
 Тест проверяет успешность добавления нового товара, количество товара в
 корзине до и после добавления""")
@allure.feature("API: Корзина товаров")
@pytest.mark.api
def test_add_to_cart(api_cart: CartApi, inside_test_data: dict) -> None:
    """
    Тест проверяет работу функционала - добавление товара в корзину.
    Сверяется количество товара в корзине до и после добавления нового
 товара.
    Проверяется, что товар успешно добавлен и количество товаров в корзине
 увеличилось на 1.
    Параметры
        api_cart: CartApi - сущность для работы класса 'CartApi'
        inside_test_data: dict - тестовые данные для запросов (id товара)
    """
    with allure.step("Перед тестированием."):
        api_cart.cart_delete_all()

    before = api_cart.cart_short()
    before_count = before.json()['data']['quantity']

    product_added_id = dict({'id': inside_test_data['id']})
    added = api_cart.add_to_cart(product_added_id)

    after = api_cart.cart_info()
    after_count = len(after.json()['products'])

    with allure.step("После тестирования."):
        api_cart.cart_delete_all()

    with allure.step("Проверки Status Code."):
        with allure.step(""""Запрос: получение информации о корзине
 до добавления. Status Code = 200"""):
            assert before.status_code == 200, f"""Ошибка при обработке
 запроса на получение информации о корзине до добавления:
   {before.status_code}"""
        with allure.step("""Запрос: добавление товара в корзину.
 Status Code = 200"""):
            assert added.status_code == 200, f"""Ошибка при обработке
 запроса на добавление товара в корзину: {added.status_code}"""
        with allure.step("""Запрос: получение информации о корзине
 после добавления. Status Code = 200"""):
            assert after.status_code == 200, f"""Ошибка ри обработке запроса
 на получениие информации о корзине после добавления: {after.status_code}"""
        with allure.step("Проверка: количество товаров увеличилось на 1"):
            subtraction = after_count - before_count
            assert subtraction == 1, f"""Ошибка:
разница в количестве товара до и после добавления : {subtraction}"""


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Проверка API: Удаление товара из корзины по ID")
@allure.description("""Проверка API для удаления товара из корзины по его ID.
 Тест проверяет количество товара в корзине до и после добавления
 нового товара""")
@allure.feature("API: Корзина товаров")
@pytest.mark.api
def test_delete_from_cart(api_cart: CartApi, inside_test_data: dict):
    """
    Тест проверяет работу функционала - удаление одного товара из корзины.
    Тест добавляет товар в корзину, затем удаляет его по ID и проверяет,
    что количество товаров уменьшилось на 1.
    Параметры:
        api_cart: CartApi - сущность для работы класса 'CartApi'
        inside_test_data: dict - тестовые данные
    """
    with allure.step("Перед тестированием."):
        api_cart.cart_delete_all()

    id_for_test = inside_test_data["id"]
    id_add = dict({"id": id_for_test})

    added = api_cart.add_to_cart(id_add)
    assert added.status_code == 200, f"""Ошибка при добавлении товара
 в корзину: {added.status_code}"""

    before = api_cart.cart_info()
    before_count = len(before.json()['products'])

    id_to_be_deleted = str(before.json()['products'][0]['id'])

    delete = api_cart.del_from_cart(id_to_be_deleted)

    after = api_cart.cart_short()
    after_count = after.json()['data']['quantity']

    with allure.step("После тестирования."):
        api_cart.cart_delete_all()

    subtraction = before_count - after_count
    with allure.step("Проверки Status Code."):
        with allure.step("""Запрос: получение информации о корзине
 до удаления. Status Code = 200"""):
            assert before.status_code == 200, f"""Ошибка при обработке
 запроса на получение информации о корзине до удаления: {before.status_code}"""
        with allure.step("""Запрос: удаление товара из корзины.
 Status Code = 204"""):
            assert delete.status_code == 204, f"""Ошибка при обработке
 запроса на удаление товара из корзины: {delete.status_code}"""
        with allure.step("""Запрос: получение информации о корзине
 после удаления. Status Code = 200"""):
            assert after.status_code == 200, f"""Ошибка при обработке запроса
 на получение информации о корзине после удаления: {after.status_code}"""
    with allure.step("Проверка: количество товаров уменьшилось на 1"):
        assert before_count - after_count == 1, f"""Ошибка:
разница в количестве товара до и после удаления : {subtraction}"""


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Проверка API: Изменение количества единиц товара")
@allure.description("""Проверка API для удаления товара из корзины по его ID.
 Тест проверяет количество единиц товара в корзине до и после изменения.""")
@allure.feature("API: Корзина товаров")
@pytest.mark.api
def test_quantity_of_product(api_cart: CartApi, inside_test_data: dict):
    """
    Тест проверяет работу функционала - изменение количества единиц товара.
    Тест добавляет товар в корзину, изменяет количество товара и проверяет,
    что количество единиц товара изменилось.
    Параметры:
        api_cart: CartApi - сущность для работы класса 'CartApi'
        inside_test_data: dict - тестовые данные
    """
    with allure.step("Перед тестированием."):
        api_cart.cart_delete_all()

    id_for_test = inside_test_data["id"]
    id_add = dict({"id": id_for_test})

    added = api_cart.add_to_cart(id_add)
    assert added.status_code == 200, f"""Ошибка при добавлении товара
    в корзину: {added.status_code}"""

    before = api_cart.cart_info()
    before_count = before.json()['products'][0]['quantity']

    param_id = before.json()['products'][0]['id']
    param_quantity = before_count + 1
    param_for_requests = ([{'id': param_id, 'quantity': param_quantity}])

    quantity = api_cart.change_product_quantity(param_for_requests)

    after = api_cart.cart_info()
    after_count = after.json()['products'][0]['quantity']

    with allure.step("После тестирования."):
        api_cart.cart_delete_all()

    with allure.step("Проверки Status Code."):
        with allure.step("""Запрос: количество единиц товара до изменения.
 Status Code = 200"""):
            assert before.status_code == 200, f"""Ошибка при обработке запроса
 о количестве единиц товара до изменения:
 Status Code = {before.status_code}"""
        with allure.step("""Запрос: изменение количества единиц товара.
 Status Code = 200"""):
            assert quantity.status_code == 200, f"""Ошибка при обработке
 запроса на изменение количества единиц товара:
 Status Code = {quantity.status_code}"""
        with allure.step("""Запрос: количество единиц товара после изменения.
 Status Code = 200"""):
            assert after.status_code == 200, f"""Ошибка при обработке запроса о
 количестве единиц товара после изменения: Status Code = {after.status_code}"""
    with allure.step("Проверка: изменилось количество единиц товара"):
        assert before_count != after_count, """Ошибка:  количество единиц
 товаров не изменилось."""


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("""Проверка API: поиск товара на главной странице
(позитивные сценарии)""")
@allure.description("""Проверка API: поиска товар на главной странице
 сайта с помощью строки поиска.
 Тест осуществляет ввод валидных значений в поле строки поиска и проверяет,
 что результат запроса содержит запрошенный контент.""")
@allure.feature("API: Поиск товара")
@pytest.mark.api
def test_search_positive(api_search: SearchApi, search_positive):
    """
    Тест осуществляет ввод валидных значений в поле строки поиска и проверяет,
    что результат запроса содержит запрошенный контент.
    Параметры:
        api_cart: CartApi - сущность для работы класса 'CartApi'
        search_positive - фикстура для получения фразы для теста
    """
    param = "phrase=" + search_positive
    response_search = api_search.search_by_phrase(param)
    search_conversion = api_search.text_conversion(search_positive)
    temp_include = response_search.json()["included"]
    temp_phrase = temp_include[0]["attributes"]["title"]

    with allure.step("Проверки выполнения запросов."):
        with allure.step("""Запрос на получение ответа о результатах поиска:
 Status Code = 200"""):
            assert response_search.status_code == 200, f"""Ошибка
 при обработке запроса на получение ответа о результатах поиска:
 Status Code = {response_search.status_code}"""

        try:
            with allure.step(f"""Проверка: результат содержит фразу поиска
             {search_conversion}."""):
                assert search_conversion in temp_phrase.lower()
        except NoSuchElementException:
            pytest.fail(
                f"В результатах поиска нет фразы: {search_conversion}.")
        except Exception as e:
            pytest.fail(f"Не удалось обработать запрос,  ошибка : {e}")
