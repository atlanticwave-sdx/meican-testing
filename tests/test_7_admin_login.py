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

class Test_7(ssl_handle.SSLBaseTest):

    # Entering valid login password and clicking sign in
    def test_admin_login_valid_login_password(self):
        self.handle_ssl_warning(urls.all_urls['ADMIN_LOGIN_URL'])
        
        login = "master"
        password = "master"
            
        self.driver.find_element(By.ID, "loginform-login").send_keys(login)
        self.driver.find_element(By.ID, "loginform-password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Dashboard')]"))
        )
        assert check_element.is_displayed(), "Dashboard element not visible after login"

        self.driver.find_element(By.XPATH, "//a[contains(text(),'Sign out')]").click()
    
if __name__ == "__main__":
    pytest.main()