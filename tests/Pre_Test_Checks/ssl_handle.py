import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


@pytest.mark.usefixtures("chrome_driver_init")
class SSLBaseTest:
    def handle_ssl_warning(self, url):
        self.driver.get(url)
        try:
            ssl_warning = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Your connection is not private')]")
            if ssl_warning:
                self.driver.find_element(By.ID, "details-button").click()
                self.driver.find_element(By.ID, "proceed-link").click()
        except NoSuchElementException:
            pass
