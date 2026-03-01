# Проект: Интернет-магазин книг “Читай-город”
"Читай-город" (https://www.chitai-gorod.ru)
Ссылка на итоговый проект https://pugapav.yonote.ru/doc/kursovaya-itogovaya-gItTQz9IFF
Видео защита итогового проекта https://disk.yandex.ru/i/xfnxlovGoUTMCw

### Шаги
1. Склонировать проект c GIT
2. Установить зависимости `pip install -r requirements.txt`
3. Для корректной работы коллекции необходимо в файле test_data.json указать актуальный токен: 
Получить его можно, используя DevTools:
- зайти [на сайт интернет-магазина "Читай-город"](https://www.chitai-gorod.ru/),
- в DevTools перейти на вкладку **Application**, далее - **Storage** - **Cookies**,
- выбрать https://www.chitai-gorod.ru,
- в части **"Name**" найти **"access-token"**, 
- внизу поставить галочку в чек-боксе **"Show URL-decoded"**,
- скопировать значение вместе со словом "Bearer",
- вставить его в файл **test_data.json** в поле **"token"**.
4. Запустить тесты:
    - все тесты:    `    python -m pytest    `

    - все UI-тесты: `    pytest -m ui     `

    - все API-тесты:`    pytest -m api    `
5. Сгенерировать отчет: `allure generate allure-files -o allure-report`
6. Открыть отчет:       `allure open allure-report`

### Структура:
- ./test - тесты
- ./ui_pages - описание страниц для UI-тестов
- ./api_utils - хелперы для работы с API
- ./configuration - провайдер настроек
- ./testdata - провайдер тестовых данных
- pytest.ini - конфигурация для запуска тестов
- test_config.ini - настройки для тестов
- test_data.json - данные для тестов
- requirements.txt - список зависимостей (библиотеки)
- README.md - описание работы с проектом
- .gitignore - файл с исключениями

