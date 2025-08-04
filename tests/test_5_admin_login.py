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

class Test_5(ssl_handle.SSLBaseTest):

    # Entering valid password blank login and clicking sign in
    def test_admin_login_valid_password_blank_admin(self, chrome_driver_init):
        # Use the fixture directly
        self.driver = chrome_driver_init

        # Handle SSL warning like the original ssl_handle does
        self.driver.get(urls.all_urls['ADMIN_LOGIN_URL'])

        # Continue with SSL warning handling if needed
        try:
            # Check for SSL warning and handle it
            proceed_button = self.driver.find_element(By.ID, "proceed-button")
            proceed_button.click()
        except:
            pass  # No SSL warning, continue

        password = "master"

        self.driver.find_element(By.ID, "loginform-password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[text()='Sign in']").click()
        
        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Login cannot be blank.')]"))
        )
        assert check_element.is_displayed(), "Login cannot be blank message not displayed"
    
if __name__ == "__main__":
    pytest.main()