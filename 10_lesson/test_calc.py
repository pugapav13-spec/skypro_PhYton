import allure
from calc.CalculatorPage import CalculatorPage


@allure.title("Тест медленного калькулятора: 7 + 8 = 15")
@allure.description("Проверка работы калькулятора с задержкой вычисления 45 секунд")
@allure.feature("Калькулятор")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("smoke", "math")
def test_slow_calculator(browser):
    """
    Тест проверяет работу калькулятора с задержкой:
    1. Установка задержки 45 секунд
    2. Вычисление 7 + 8
    3. Ожидание результата 15
    4. Проверка полученного результата
    """
    with allure.step("Инициализация страницы калькулятора"):
        calculator_page = CalculatorPage(browser)
        allure.attach(
            "URL: https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html",
            name="Страница",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Выполнение операции 7 + 8 с задержкой 45 секунд"):
        calculator_page.calculate_7_plus_8(delay_seconds=45)
    
    with allure.step("Ожидание результата 15 (таймаут 50 секунд)"):
        calculator_page.wait_for_result("15", timeout=50)
    
    with allure.step("Получение фактического результата"):
        final_result = calculator_page.get_result()
        
        with allure.step("Проверка результата"):
            allure.attach(
                f"Ожидалось: 15\nПолучено: {final_result}",
                name="Сравнение",
                attachment_type=allure.attachment_type.TEXT
            )
            assert final_result == "15", f"Ожидалось 15, получено {final_result}"
    
    with allure.step("Тест успешно завершен"):
        allure.attach(
            "Калькулятор работает корректно с задержкой 45 секунд",
            name="Результат",
            attachment_type=allure.attachment_type.TEXT
        )
