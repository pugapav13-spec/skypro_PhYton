import allure
import pytest
from ui_pages.BasePage import BasePage
from ui_pages.MainPage import MainPage
from ui_pages.CartPage import CartPage
from ui_pages.ProductPage import ProductPage
from selenium.webdriver.common.by import By


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("""UI: Добавление товара в корзину из карточки товара""")
@allure.description("""UI: "Проверяет наличие в корзине товара,
 добавленного из карточки товара.""")
@allure.feature("UI: Корзина товаров")
@pytest.mark.ui
def test_added_to_cart_from_product_page(browser) -> None:
    """
    Добавление товара в корзину из карточки товара и
    проверка его наличия в корзине.
    Тест выполняет:
    - переход в карточку товара (первого на главной странице),
    - добавление товара в корзину по кнопке "Купить",
    - проверка наличия выбранного товара в корзине по наименованию.
        return: None
    """
    try:
        main_page = MainPage(browser)
        cart_page = CartPage(browser)
        product_page = ProductPage(browser)

        main_page.go_base_url()

        with allure.step("""Запомнить данные первого товара, отображаемого
 в списке товаров на странице."""):
            locator = (By.CLASS_NAME, "product-card__title")
            product_url = main_page.get_element_attribute(locator, "href")
            product_name = main_page.get_element_attribute(locator, "text")

        with allure.step("Перейти в карточку товара"):
            product_page.go_to_url(product_url)

        with allure.step("Добавить товар в корзину"):
            locator = (By.CLASS_NAME, "product-offer-button")
            product_page.buy_product()

        cart_page.go_to_cart()

        with allure.step("Проверка: товар отображается в корзине"):
            assert cart_page.check_product_in_cart(
                product_name), f"В корзине отсутствует товар '{product_name}'"
    except Exception:
        raise


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("UI:  Поиск товара на главной странице (позитивные сценарии)")
@allure.description(
    """UI: Проверка функционала поиска товара на главной странице сайта
 с помощью строки поиска (позитивные сценарии).
 Тест осуществляет ввод валидных значений в поле строки поиска и проверяет
 ожидаемый результат запроса - строка с информацией о наличии контента.""")
@allure.feature("UI: Поиск товара")
@allure.step("UI: Ввод валидных значений в строку поиска")
@pytest.mark.ui
def test_search_positive(browser, search_positive) -> None:
    """
    Проверка функционала поиска товара на главной странице сайта с помощью
    строки поиска.
    Тест осуществляет ввод валидных значений из параметров в поле строки
    поиска и проверяет, что получен результат запроса -
    строка с информацией о наличии контента.
        search_positive: фикстура для получения валидных тестовых данных
                         для поля "Поиск" из файла test_data.json.
        return: None
    """
    main_page = MainPage(browser)

    main_page.go_base_url()

    response_search = main_page.search_by_phrase(search_positive)

    with allure.step("Проверка: есть сообщение о наличии контента."):
        err_message = "Не найдено сообщение о наличии контента"
        assert "найдено" in response_search, err_message


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("""UI: Поиск товара на главной странице (негативные сценарии)""")
@allure.description("""Проверка функционала поиска товара на главной странице
 сайта с помощью строки поиска (негативные сценарии).
 Тест осуществляет ввод невалидных значений в поле строки поиска и проверяет
 ожидаемый результат запроса - строка с информацией, что поиск не принес
 результатов.""")
@allure.feature("UI: Поиск товара")
@pytest.mark.ui
def test_search_negative(browser, search_negative) -> None:
    """
    Тест осуществляет ввод невалидных значений в поле строки поиска и
 проверяет, что получен результат запроса - строка с информацией об отсутствии
 найденного контента.
        search_negative: фикстура для получения невалидных тестовых данных
                         для поля "Поиск" из файла test_data.json.
        return: None
    """
    main_page = MainPage(browser)

    main_page.go_base_url()

    response_search = main_page.search_by_phrase(search_negative)

    with allure.step("Проверка, что результат поиска не принёс результатов."):
        error_message = "Невалидный запрос поиска вернул результаты"
        assert "не принёс результатов" in response_search, error_message


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("UI: Проверка навигации - переход по разделам сайта")
@allure.description("""UI: Проверка функционала перехода по разделам сайта.
 Тест осуществляет переход по основным разделам сайта и проверку нахождения
 на нужной странице.""")
@allure.feature("UI: Навигация по сайту")
@pytest.mark.parametrize("navigation", [
    ["Акции", "/promotions"],
    ["Распродажа", "/sales"],
    ["Комиксы и манга", "/comics"],
    ["Настольные игры", "/nastolnyj-klub"],
    ["Что ещё почитать?", "/collections"],
    ["Читай-журнал", "/articles"],
    ["Подарочные сертификаты", "/certificate"]
    ])
@pytest.mark.ui
def test_navigation(browser, navigation: list) -> None:
    """
    Тест осуществляет переход по страницам сайта по основным разделам меню.
    Проверка, что открылась нужная страница, проводится по наименованию
    активной вкладки.
        navigation: list - список тестовых данных, содержит:
                    - наименование страниц сайта,
                    - endpoint URL для перехода на страницу сайта.
    """
    base_page = BasePage(browser)

    try:
        with allure.step("""Получить данных для теста -
        URL и наименование вкладки."""):
            test_text = navigation[0]
            test_url = base_page.base_url + navigation[1]

        base_page.go_to_url(test_url)

        param = "header-bottom__link.nuxt-link-exact-active.nuxt-link-active"
        locator = (By.CLASS_NAME, (param))

        current_text = base_page.get_element_attribute(locator, "text")

        with allure.step(f"""Страница {test_url} соответствует вкладке
         {test_text}."""):
            assert test_text in current_text, f"""Текущая страница
            {test_url} не соответствует вкладке {test_text}"""
    except Exception as e:
        raise Exception(f"Произошла ошибка: {e}")


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("""UI: Проверка неактивности кнопки 'Получить код'
 при вводе невалидного номера телефона""")
@allure.description("""Проверяется поведение кнопки 'Получить код'
 при вводе невалидных значений в поле номера телефона.
 Ожидается, что кнопка будет неактивна, если введено невалидное значение.""")
@allure.feature("UI: Авторизация пользователя")
@pytest.mark.ui
def test_number_phone_invalid(browser, number_phone_invalid) -> None:
    """
    Тест проверяет ожидаемое поведение кнопки 'Получить код'
    при вводе невалидных значений в поле номера телефона.
    В шагах теста осуществляется:
    - ввод невалидного номера телефона (из списка невалидных данных),
    - проверка, что кнопка 'Получить код' неактивна.
        number_phone_invalid: фикстура для получения тестовых невалидных
                     данных для поля "Номер телефона" из файла test_data.json.
    """
    main_page = MainPage(browser)

    main_page.go_base_url()

    with allure.step("Нажать на кнопку 'Войти'."):
        # локатор для кнопки "Войти"
        atribute = "button.header-controls__btn[aria-label='Меню профиля']"
        locator = (By.CSS_SELECTOR, atribute)
        main_page.click_element(locator)

        # локатор для поля ввода
        locator = (By.ID, 'tid-input')
        main_page.enter_text(locator, number_phone_invalid)

        # локатор для кнопки 'Получить код'
        atribute = "button.auth-modal-content__button"
        locator = (By.CSS_SELECTOR, atribute)

        is_button_disabled = main_page.element_disabled(locator)

    with allure.step("Проверка: состояние кнопки 'Получить код' - активна"):
        assert is_button_disabled is not None, """Кнопка 'Получить код'
        должна быть неактивна для невалидных значений."""
