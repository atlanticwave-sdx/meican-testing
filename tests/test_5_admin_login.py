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
    def test_admin_login_valid_password_blank_admin(self):
        self.handle_ssl_warning(urls.all_urls['ADMIN_LOGIN_URL'])

        password = "master"

        self.driver.find_element(By.ID, "loginform-password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[text()='Sign in']").click()
        
        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Login cannot be blank.')]"))
        )
        assert check_element.is_displayed(), "Login cannot be blank message not displayed"
    
if __name__ == "__main__":
    pytest.main()