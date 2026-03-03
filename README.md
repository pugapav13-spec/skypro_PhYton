# Проект: Интернет-магазин книг “Читай-город”
"Читай-город" (https://www.chitai-gorod.ru)
Ссылка на итоговый проект https://pugapav.yonote.ru/doc/kursovaya-itogovaya-gItTQz9IFF
Видео защита итогового проекта https://disk.yandex.ru/i/xfnxlovGoUTMCw

### Шаги

Установка зависимостей pip install -r requirements.txt
Все тесты pytest
Только UI‑тесты pytest -m ui -v
Только API‑тесты pytest -m api -v
С отчётом Allure pytest --alluredir=allure-results allure serve allure-results


Получение токена авторизации для API-тестов
Для корректной работы API-тестов необходимо указать актуальный Bearer-токен в файле conftest.py:
Откройте сайт интернет-магазина "Читай-город" https://www.chitai-gorod.ru/ в браузере Chrome
Откройте инструменты разработчика (DevTools): F12 или Ctrl+Shift+I
Перейдите на вкладку Network (Сеть)
Обновите страницу (F5) и найдите запрос к auth-issues или любой запрос с заголовком authorization
В заголовках запроса (Request Headers) найдите поле authorization
Скопируйте значение без слова "Bearer" (только сам токен)
Вставьте скопированное значение в файл conftest.py в поле BEARER_TOKEN

Структура:
config.py – настройки окружения
data.py – тестовые данные
pages/ – Page Object для UI‑тестов
api/ – клиент для работы с API
tests/test_ui.py – UI‑тесты поиска (6 шт.)
tests/test_api.py – API‑тесты корзины (6 шт.)
conftest.py – фикстуры pytest
pytest.ini – маркеры для раздельного запуска
requirements.txt – зависимости

Стек:
pytest selenium webdriver manager requests allure configparser json re