from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from shop.AuthorizationPage import AuthorizationPage
from shop.MainPage import MainPage
from shop.CartPage import CartPage
from shop.Order import Order


def test_shop():
    browser = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install())
    )

    login = AuthorizationPage(browser)
    login.login_account('standard_user', 'secret_sauce')

    main_page = MainPage(browser)
    added_products = main_page.add_products()
    main_page.go_to_cart()

    cart_page = CartPage(browser)
    cart_items = cart_page.get_cart_items()
    assert set(cart_items) == set(added_products)
    cart_page.click_checkout()

    order = Order(browser)
    order.making_in_order('Иван', 'Иванов', '123')
    total_text = order.summary_amount()
    total_amount = total_text.split("$")[1]
    assert total_amount == "58.29"

    browser.close()
