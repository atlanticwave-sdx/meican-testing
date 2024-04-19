import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from Pre_Test_Checks.ssl_handle import SSLBaseTest
from Web_Driver.conftest import chrome_driver_init
from URLS.urls import all_urls


class Test_7(SSLBaseTest):

    # Test -7 --> Entering correct login and password credentials and clicking signup button
    def test_admin_login_singup_all_correct_credentials_signup_button_check(self):
        self.handle_ssl_warning(all_urls['ADMIN_LOGIN_URL'])
        
        self.driver.find_element(By.ID, "loginform-login").send_keys("master")
        self.driver.find_element(By.ID, "loginform-password").send_keys("master")
        self.driver.find_element(By.XPATH, "//button[text()='Sign in']").click()
        
        check_element1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Dashboard')]"))
        )
        assert check_element1.is_displayed(), "Dashboard element not visible after login"
        
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Sign out')]").click()
        
if __name__ == "__main__":
    pytest.main()