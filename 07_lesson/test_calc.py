from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from calc.CalculatorPage import CalculatorPage


def test_slow_calculator():
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )
    calculator_page = CalculatorPage(browser)
    calculator_page.calculate_7_plus_8(delay_seconds=45)
    calculator_page.wait_for_result("15", timeout=50)
    final_result = calculator_page.get_result()
    assert final_result == "15"

    browser.quit()
