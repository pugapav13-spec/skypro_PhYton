# Убраны прямые вызовы WebDriver - используются фикстуры
def test_shop(firefox_driver):  # Используем фикстуру вместо создания драйвера
    """Тест интернет-магазина Sauce Demo"""
    
    # Авторизация
    from shop.AuthorizationPage import AuthorizationPage
    login = AuthorizationPage(firefox_driver)
    login.login_account('standard_user', 'secret_sauce')
    
    # Добавление товаров
    from shop.MainPage import MainPage
    main_page = MainPage(firefox_driver)
    added_products = main_page.add_products()
    main_page.go_to_cart()
    
    # Проверка корзины
    from shop.CartPage import CartPage
    cart_page = CartPage(firefox_driver)
    cart_items = cart_page.get_cart_items()
    
    # Assert проверки остаются - это часть тестовой логики
    assert set(cart_items) == set(added_products)
    cart_page.click_checkout()
    
    # Оформление заказа
    from shop.Order import Order
    order = Order(firefox_driver)
    order.making_in_order('Иван', 'Иванов', '123')
    
    # Проверка суммы
    total_text = order.summary_amount()
    total_amount = total_text.split("$")[1]
    assert total_amount == "58.29"
    # Браузер автоматически закрывается фикстурой - убран browser.close()


# Тест с Chrome браузером через фикстуру browser
def test_shop_chrome(browser):  # Используем фикстуру browser (Chrome по умолчанию)
    """Тест интернет-магазина с Chrome браузером"""
    
    from shop.AuthorizationPage import AuthorizationPage
    from shop.MainPage import MainPage
    from shop.CartPage import CartPage
    from shop.Order import Order
    
    # Авторизация
    login = AuthorizationPage(browser)
    login.login_account('standard_user', 'secret_sauce')
    
    # Добавление товаров
    main_page = MainPage(browser)
    added_products = main_page.add_products()
    main_page.go_to_cart()
    
    # Проверка корзины
    cart_page = CartPage(browser)
    cart_items = cart_page.get_cart_items()
    
    # Assert проверки
    assert set(cart_items) == set(added_products)
    cart_page.click_checkout()
    
    # Оформление заказа
    order = Order(browser)
    order.making_in_order('Иван', 'Иванов', '123')
    total_text = order.summary_amount()
    total_amount = total_text.split("$")[1]
    assert total_amount == "58.29"
    # Браузер автоматически закрывается фикстурой
