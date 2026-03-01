import requests
import allure


class BaseApi:
    """
    Класс содержит общие методы для базовых API-запросов:
    - Получить текущий URL,
    - Добавление товара в корзину по артикулу (id).
    """
    @allure.step("""BaseApi. URL:{base_url}, {track_url},
                 параметры для авторизации: {params}""")
    def __init__(self, base_url: str, track_url: str, params: dict) -> None:
        """
        Инициализация метода 'BaseApi'.
        Определяет сущность класса 'BaseApi' и формирует
        параметры для requests-запросов:
        base_url: str - основной URL сайта,
        track_url: str - URL для запроса - определение текущего URL,
        params: dict - словарь с необходимыми для авторизации данными,
                        содержит ключи:
                        - token: str,
                        - user_agent: str,
                        - content_type: str.
        """
        self.base_url = base_url
        self.track_url = track_url
        self.params = params

    @allure.step("Получить текущий URL вида https://www.chitai-gorod.ru...")
    def current_url(self) -> str:
        path = self.track_url
        resp = requests.get(path, headers=self.params)
        current_url = resp['requestUri']
        return current_url
