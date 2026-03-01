import json

with open('test_data.json', encoding='utf-8') as test_data:
    global_data = json.load(test_data)


class DataProvider:

    def __init__(self) -> None:
        self.data = global_data

    def get(self, prop: str) -> str:
        return self.data.get(prop)

    def getint(self, prop: str) -> int:
        val = self.data.get(prop)
        return int(val)

    def get_list(self, prop: str):
        """Получает список по ключу из файла данных."""
        data = self.get(prop)
        if not isinstance(data, list):
            raise TypeError(f"Ожидается список для ключа '{prop}',\
                            но получен {type(data)}")
        return data

    def get_token(self) -> str:
        return self.data.get("token")

    def get_user_agent(self) -> str:
        return self.data.get("user_agent")

    def get_content_type(self) -> str:
        return self.data.get("content_type")
