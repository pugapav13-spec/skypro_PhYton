import allure
from shop.AuthorizationPage import AuthorizationPage
from shop.MainPage import MainPage
from shop.CartPage import CartPage
from shop.Order import Order


@allure.title("Тест оформления заказа в интернет-магазине")
@allure.description("Проверка полного цикла покупки: авторизация, добавление товаров, проверка корзины и оформление заказа")
@allure.feature("Магазин")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "regression")
@allure.link("https://www.saucedemo.com/", name="Sauce Demo")
def test_shop(firefox_driver):
    """
    Тест проверяет сценарий покупки в интернет-магазине:
    1. Авторизация пользователя
    2. Добавление товаров в корзину
    3. Проверка содержимого корзины
    4. Оформление заказа
    5. Проверка итоговой суммы
    """
    browser = firefox_driver
    
    # Шаг 1: Авторизация
    with allure.step("Авторизация в системе"):
        login = AuthorizationPage(browser)
        login.login_account('standard_user', 'secret_sauce')
    
    # Шаг 2: Добавление товаров
    with allure.step("Добавление товаров в корзину"):
        main_page = MainPage(browser)
        added_products = main_page.add_products()
        main_page.go_to_cart()
    
    # Шаг 3: Проверка корзины
    with allure.step("Проверка содержимого корзины"):
        cart_page = CartPage(browser)
        cart_items = cart_page.get_cart_items()
    
    # Шаг 4: Проверка соответствия товаров
    with allure.step("Сравнение добавленных товаров с товарами в корзине"):
        allure.attach(
            f"Добавлено: {added_products}\nВ корзине: {cart_items}",
            name="Сравнение списков",
            attachment_type=allure.attachment_type.TEXT
        )
        assert set(cart_items) == set(added_products), \
            f"Товары не совпадают. Добавлено: {added_products}, В корзине: {cart_items}"
        cart_page.click_checkout()
    
    # Шаг 5: Оформление заказа
    with allure.step("Заполнение данных для заказа"):
        order = Order(browser)
        order.making_in_order('Иван', 'Иванов', '123')
    
    # Шаг 6: Проверка итоговой суммы
    with allure.step("Проверка итоговой суммы заказа"):
        total_text = order.summary_amount()
        total_amount = total_text.split("$")[1]
        
        allure.attach(
            f"Ожидаемая сумма: $58.29\nФактическая сумма: ${total_amount}",
            name="Проверка суммы",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert total_amount == "58.29", \
            f"Неверная итоговая сумма. Ожидалось: 58.29, Получено: {total_amount}"
    
    with allure.step("Тест успешно завершен"):
        allure.attach(
            "Все проверки пройдены успешно",
            name="Результат",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.title("Тест магазина с Chrome браузером")
@allure.description("Проверка интернет-магазина с использованием Chrome браузера")
@allure.feature("Магазин")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("cross-browser")
def test_shop_chrome(browser):
    """
    Тест проверяет работу магазина в Chrome браузере.
    """
    with allure.step("Запуск теста в Chrome браузере"):
        allure.attach(
            "Браузер: Chrome",
            name="Информация",
            attachment_type=allure.attachment_type.TEXT
        )
    
    # Шаг 1: Авторизация
    with allure.step("Авторизация пользователя"):
        login = AuthorizationPage(browser)
        login.login_account('standard_user', 'secret_sauce')
    
    # Шаг 2: Добавление товаров
    with allure.step("Добавление товаров в корзину"):
        main_page = MainPage(browser)
        added_products = main_page.add_products()
        main_page.go_to_cart()
    
    # Шаг 3: Проверка корзины
    with allure.step("Проверка содержимого корзины"):
        cart_page = CartPage(browser)
        cart_items = cart_page.get_cart_items()
        
        with allure.step("Проверка соответствия товаров"):
            assert set(cart_items) == set(added_products)
            cart_page.click_checkout()
    
    # Шаг 4: Оформление заказа
    with allure.step("Оформление заказа"):
        order = Order(browser)
        order.making_in_order('Иван', 'Иванов', '123')
        
        with allure.step("Проверка итоговой суммы"):
            total_text = order.summary_amount()
            total_amount = total_text.split("$")[1]
            assert total_amount == "58.29"
