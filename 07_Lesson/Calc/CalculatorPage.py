from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        )
        self.waiter = WebDriverWait(driver, 50)

    def set_delay(self, delay_seconds):
        self.waiter.until(EC.presence_of_element_located((By.ID, "delay")))
        delay_input = self.driver.find_element(By.ID, "delay")
        delay_input.clear()
        delay_input.send_keys(str(delay_seconds))
        return self

    def click_button(self, button_text):
        button = self.driver.find_element(
            By.XPATH, f"//span[text()='{button_text}']"
        )
        button.click()
        return self

    def press_7(self):
        return self.click_button("7")

    def press_8(self):
        return self.click_button("8")

    def press_plus(self):
        return self.click_button("+")

    def press_equals(self):
        return self.click_button("=")

    def get_result(self):
        result_element = self.driver.find_element(By.CLASS_NAME, "screen")
        return result_element.text

    def wait_for_result(self, expected_result, timeout=None):
        if timeout is None:
            timeout = 50

        waiter = WebDriverWait(self.driver, timeout)

        waiter.until(
            lambda d: d.find_element(
                By.CLASS_NAME, "screen").text == str(expected_result)
        )

    def calculate_7_plus_8(self, delay_seconds=45):
        self.set_delay(delay_seconds)
        self.press_7()
        self.press_plus()
        self.press_8()
        self.press_equals()
        return self
