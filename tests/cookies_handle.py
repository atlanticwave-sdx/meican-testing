import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

@pytest.mark.usefixtures("chrome_driver_init")
class CookiesBaseTest:
    def handle_cookies_warning(self, url):
        self.driver.get(url)
        sleep(1)
        try:
            ssl_warning = self.driver.find_element(By.XPATH, "//h2[@id='onetrust-policy-title']")
            if ssl_warning:
                self.driver.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']").click()
        except NoSuchElementException:
            pass