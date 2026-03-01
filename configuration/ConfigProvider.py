import configparser

global_config = configparser.ConfigParser()
global_config.read("test_config.ini")


class ConfigProvider:
    """
    Класс настройки конфигурации проекта
    """

    def __init__(self):
        self.config = global_config

    def get(self, section: str, prop: str):
        """
        Метод возвращает заданное значение из файла test_config.ini
        для использования в работе:
            section: str - секция UI или API
            prop: str - свойство для настройки работы
                    (напр., URL, endpoint, timeout)
        """
        return self.config[section].get(prop)

    def getint(self, section: str, prop: int):
        return self.config[section].getint(prop)

    # специальные методы
    # UI: создание URL для перехода по страницам сайта
    def get_ui_url(self, url) -> str:
        return self.config["ui"].get(url)

    # API: base_url
    def get_api_url(self, endpoint: None) -> str:
        base_url = self.config["api"].get("base_url")
        if endpoint is None:
            resp = base_url
        else:
            resp = base_url + self.config["api"].get(endpoint)
        return resp
