import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Order:
    """
    Page Object для страницы оформления заказа.
    Содержит методы для заполнения информации о покупателе и проверки итоговой суммы.
    """
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы оформления заказа.
        
        Args:
            driver: WebDriver экземпляр браузера
        """
        self.driver = driver
        self._first_name = (By.ID, "first-name")
        self._last_name = (By.ID, "last-name")
        self._postal_code = (By.ID, "postal-code")
        self._continue_button = (By.ID, "continue")
        self._summary_total = (By.CSS_SELECTOR, ".summary_total_label")
        self._finish_button = (By.ID, "finish")
    
    @allure.step("Заполнение данных для заказа")
    def making_in_order(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Заполняет форму с данными покупателя и подтверждает заказ.
        
        Args:
            first_name: Имя покупателя
            last_name: Фамилия покупателя
            postal_code: Почтовый индекс
            
        Returns:
            None
        """
        with allure.step(f"Ввод имени: {first_name}"):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self._first_name)
            ).send_keys(first_name)
        
        with allure.step(f"Ввод фамилии: {last_name}"):
            self.driver.find_element(*self._last_name).send_keys(last_name)
        
        with allure.step(f"Ввод почтового индекса: {postal_code}"):
            self.driver.find_element(*self._postal_code).send_keys(postal_code)
        
        with allure.step("Переход к следующему шагу"):
            self.driver.find_element(*self._continue_button).click()
        
        allure.attach(
            f"Данные заказа: {first_name} {last_name}, индекс: {postal_code}",
            name="Информация о покупателе",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.step("Получение итоговой суммы заказа")
    def summary_amount(self) -> str:
        """
        Получает текст с итоговой суммой заказа.
        
        Returns:
            str: Текст с итоговой суммой (например, "Total: $58.29")
        """
        total_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self._summary_total)
        )
        total_text = total_element.text
        
        allure.attach(
            f"Итоговая сумма: {total_text}",
            name="Сумма заказа",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return total_text
