import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    """
    Page Object для страницы медленного калькулятора.
    Содержит методы для выполнения арифметических операций и получения результатов.
    """
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы калькулятора.
        
        Args:
            driver: WebDriver экземпляр браузера
        """
        self.driver = driver
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        self._delay_input = (By.ID, "delay")
        self._buttons = {
            "7": (By.XPATH, "//span[text()='7']"),
            "8": (By.XPATH, "//span[text()='8']"),
            "+": (By.XPATH, "//span[text()='+']"),
            "=": (By.XPATH, "//span[text()='=']")
        }
        self._result = (By.CSS_SELECTOR, ".screen")
    
    @allure.step("Вычисление 7 + 8 с задержкой {delay_seconds} секунд")
    def calculate_7_plus_8(self, delay_seconds: int) -> None:
        """
        Выполняет вычисление 7 + 8 на калькуляторе с заданной задержкой.
        
        Args:
            delay_seconds: Задержка вычисления в секундах
            
        Returns:
            None
        """
        with allure.step(f"Установка задержки: {delay_seconds} секунд"):
            delay_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self._delay_input)
            )
            delay_input.clear()
            delay_input.send_keys(str(delay_seconds))
        
        with allure.step("Нажатие кнопки 7"):
            self.driver.find_element(*self._buttons["7"]).click()
        
        with allure.step("Нажатие кнопки +"):
            self.driver.find_element(*self._buttons["+"]).click()
        
        with allure.step("Нажатие кнопки 8"):
            self.driver.find_element(*self._buttons["8"]).click()
        
        with allure.step("Нажатие кнопки ="):
            self.driver.find_element(*self._buttons["="]).click()
        
        allure.attach(
            f"Запущено вычисление 7 + 8 с задержкой {delay_seconds}с",
            name="Операция",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.step("Ожидание результата {expected_result}")
    def wait_for_result(self, expected_result: str, timeout: int) -> None:
        """
        Ожидает появления ожидаемого результата на экране калькулятора.
        
        Args:
            expected_result: Ожидаемое значение (например, "15")
            timeout: Максимальное время ожидания в секундах
            
        Returns:
            None
        """
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(self._result, expected_result)
        )
        allure.attach(
            f"Получен ожидаемый результат: {expected_result}",
            name="Результат",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.step("Получение текущего результата")
    def get_result(self) -> str:
        """
        Получает текущее значение на экране калькулятора.
        
        Returns:
            str: Текст с текущим результатом
        """
        result_text = self.driver.find_element(*self._result).text
        allure.attach(
            f"Текущий результат: {result_text}",
            name="Значение на экране",
            attachment_type=allure.attachment_type.TEXT
        )
        return result_text
