import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import ssl_handle
from conftest import chrome_driver_init
import urls

class Test_1(ssl_handle.SSLBaseTest):

    # Entering all blank credentials for login password fields and clicking sign in
    def test_admin_login_all_blank_credentials(self):
        self.handle_ssl_warning(urls.all_urls['ADMIN_LOGIN_URL'])

        self.driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

        check_element1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Login cannot be blank.')]"))
        )
        check_element2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Password cannot be blank.')]"))
        )
        assert check_element1.is_displayed() and check_element2.is_displayed(), "Login and Password blank messages not displayed"


if __name__ == "__main__":
    pytest.main()