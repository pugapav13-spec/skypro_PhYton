# Проект автоматизации тестирования

## Описание проекта
Проект содержит автоматические тесты для:
- Калькулятора с задержкой (https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html)
- Интернет-магазина Sauce Demo (https://www.saucedemo.com/)

Структура проекта
10_lesson/
├── calc/                    # Page Objects для калькулятора
│   └── CalculatorPage.py    # Класс страницы калькулятора
├── shop/                    # Page Objects для магазина
│   ├── AuthorizationPage.py # Страница авторизации
│   ├── MainPage.py         # Главная страница
│   ├── CartPage.py         # Страница корзины
│   └── Order.py            # Страница оформления заказа
├── conftest.py              # Фикстуры pytest
├── test_calc.py            # Тесты калькулятора
├── test_shop.py            # Тесты магазина
├── requirements.txt        # Зависимости проекта
└── README.md               # Документация

Запуск всех тестов:
pytest

Запуск конкретного теста:
pytest test_calc.py::test_slow_calculator -v
pytest test_shop.py::test_shop -v

Запуск с формированием Allure отчета:
# Выполнить тесты с сохранением результатов
pytest --alluredir=allure-results

# Просмотреть отчет (требуется установленный Allure)
allure serve allure-results

Запуск в разных браузерах:
# Firefox (по умолчанию)
pytest test_shop.py::test_shop

# Chrome
pytest test_shop.py::test_shop_chrome

Просмотр Allure отчетов
# Вариант 1: Запустить тесты и открыть отчет
pytest --alluredir=allure-results
allure serve allure-results

# Вариант 2: Сгенерировать отчет и открыть в браузере
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
