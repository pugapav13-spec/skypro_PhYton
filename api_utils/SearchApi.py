import requests
import allure
import re


class SearchApi:
    """
    Класс с методами для API-запросов при работе со страницей поиска.
    - Поиск товара
    """
    @allure.step("""SearchApi. URL: {search_url},
                 параметры для авторизации: {params}""")
    def __init__(self, search_url: str, params: dict) -> None:
        """
        Инициализация метода 'SearchApi'.
        Определяет сущность класса 'SearchApi' и формирует
        параметры для requests-запросов:
            search_url: str - основной URL для работы с поиском,
            params: dict - словарь с необходимыми для авторизации данными,
                            содержит ключи:
                            - token: str,
                            - user_agent: str,
                            - content_type: str.
        """
        self.search_url = search_url
        self.params = params

    @allure.step("Преобразование текстов - удаление лишних пробелов")
    def text_conversion(self, text: str) -> str:
        """
        Преобразует текст, делая все буквы прописными\
            и удаляя лишние пробелы между словами.
            text: str - исходный текст.
            returns: ыек - преобразованный текст.
        """
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text.lower()

    @allure.step("Поиск товара на главной странице сайта")
    def search_by_phrase(self, parameters: str):
        path = self.search_url
        response_search = requests.get(
            path, headers=self.params, params=parameters)
        return response_search
