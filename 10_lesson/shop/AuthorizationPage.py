import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthorizationPage:
    """
    Page Object для страницы авторизации интернет-магазина Sauce Demo.
    Предоставляет методы для взаимодействия с формой входа.
    """
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы авторизации.
        
        Args:
            driver: WebDriver экземпляр браузера
        """
        self.driver = driver
        self._username_input = (By.ID, "user-name")
        self._password_input = (By.ID, "password")
        self._login_button = (By.ID, "login-button")
    
    @allure.step("Авторизация пользователя {username}")
    def login_account(self, username: str, password: str) -> None:
        """
        Выполняет авторизацию пользователя в системе.
        
        Args:
            username: Имя пользователя (логин)
            password: Пароль пользователя
            
        Returns:
            None
        """
        with allure.step("Ввод имени пользователя"):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self._username_input)
            ).send_keys(username)
        
        with allure.step("Ввод пароля"):
            self.driver.find_element(*self._password_input).send_keys(password)
        
        with allure.step("Нажатие кнопки входа"):
            self.driver.find_element(*self._login_button).click()
        
        allure.attach(
            f"Авторизация выполнена с логином: {username}",
            name="Результат авторизации",
            attachment_type=allure.attachment_type.TEXT
        )
