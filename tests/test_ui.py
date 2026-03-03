import allure
import pytest
from pages.search_page import SearchPage
from data import (
    EXACT_TITLE, PARTIAL_TITLE, AUTHOR_NAME,
    SPECIAL_CHARS, NONEXISTENT_BOOK, EMPTY_QUERY
)


@pytest.mark.ui
class TestSearch:

    @allure.title("Поиск по точному названию книги")
    def test_search_exact_title(self, driver):
        """
        Тест: поиск по точному названию книги.
        Шаги:
        1. Открыть главную страницу.
        2. Ввести точное название книги.
        3. Нажать кнопку поиска.
        4. Проверить, что найдено больше 0 товаров.
        """
        page = SearchPage(driver)
        page.open()
        page.search(EXACT_TITLE)
        count = page.get_results_count()

        with allure.step(f"Проверить, что найдено товаров: {count}"):
            assert count > 0, f"По запросу '{EXACT_TITLE}' ничего не найдено"

    @allure.title("Поиск по части названия")
    def test_search_partial_title(self, driver):
        """
        Тест: поиск по части названия.
        Шаги:
        1. Открыть главную страницу.
        2. Ввести часть названия.
        3. Нажать поиск.
        4. Проверить, что найдено больше 0 товаров.
        """
        page = SearchPage(driver)
        page.open()
        page.search(PARTIAL_TITLE)
        count = page.get_results_count()

        with allure.step(f"Проверить, что найдено товаров: {count}"):
            assert count > 0, f"По запросу '{PARTIAL_TITLE}' ничего не найдено"

    @allure.title("Поиск по фамилии автора")
    def test_search_author(self, driver):
        """
        Тест: поиск по фамилии автора.
        Шаги:
        1. Открыть главную страницу.
        2. Ввести фамилию автора.
        3. Нажать поиск.
        4. Проверить, что найдено больше 0 товаров.
        """
        page = SearchPage(driver)
        page.open()
        page.search(AUTHOR_NAME)
        count = page.get_results_count()

        with allure.step(f"Проверить, что найдено товаров: {count}"):
            assert count > 0, f"По автору '{AUTHOR_NAME}' ничего не найдено"

    @allure.title("Поиск со спецсимволами")
    def test_search_special_chars(self, driver):
        """
        Тест: поиск со спецсимволами.
        Шаги:
        1. Открыть главную страницу.
        2. Ввести спецсимволы.
        3. Нажать поиск.
        4. Проверить, что найдено 0 товаров.
        """
        page = SearchPage(driver)
        page.open()
        page.search(SPECIAL_CHARS)
        count = page.get_results_count()

        with allure.step(f"Проверить, что найдено товаров: {count}"):
            assert count == 0, f"По спецсимволам найдено товаров: {count}"

    @allure.title("Поиск несуществующей книги")
    def test_search_nonexistent_book(self, driver):
        """
        Тест: поиск несуществующей книги.
        Шаги:
        1. Открыть главную страницу.
        2. Ввести несуществующее название.
        3. Нажать поиск.
        4. Проверить, что найдено 0 товаров.
        """
        page = SearchPage(driver)
        page.open()
        page.search(NONEXISTENT_BOOK)
        count = page.get_results_count()

        with allure.step(f"Проверить, что найдено товаров: {count}"):
            assert count == 0, f"По запросу найдено товаров: {count}"

    @allure.title("Пустой поисковый запрос")
    def test_search_empty_query(self, driver):
        """
        Тест: пустой поисковый запрос.
        Шаги:
        1. Открыть главную страницу.
        2. Оставить поле пустым и нажать поиск.
        3. Проверить, что найдено 0 товаров.
        """
        page = SearchPage(driver)
        page.open()
        page.search(EMPTY_QUERY)
        count = page.get_results_count()

        with allure.step(f"Проверить, что найдено товаров: {count}"):
            assert count == 0, f"При пустом запросе найдено товаров: {count}"
