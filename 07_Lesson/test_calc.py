# Убраны прямые вызовы WebDriver - используются фикстуры
def test_slow_calculator(browser):  # Используем фикстуру вместо создания драйвера
    """Тест медленного калькулятора"""
    
    from calc.CalculatorPage import CalculatorPage
    
    calculator_page = CalculatorPage(browser)
    calculator_page.calculate_7_plus_8(delay_seconds=45)
    calculator_page.wait_for_result("15", timeout=50)
    final_result = calculator_page.get_result()
    
    # Assert проверка остается
    assert final_result == "15"
    # Браузер автоматически закрывается фикстурой - убран browser.quit()
