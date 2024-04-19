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


class Test_3(SSLBaseTest):

    # Test -3 --> Entering blank login credentials and wrong password and clicking sign in
    def test_admin_login_singup_login_field_blank_and_wrong_password_credentials(self):
        self.handle_ssl_warning(all_urls['ADMIN_LOGIN_URL'])
        
        self.driver.find_element(By.ID, "loginform-password").send_keys("password")
        self.driver.find_element(By.XPATH, "//button[text()='Sign in']").click()
        
        check_element1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Login cannot be blank.')]"))
        )
        assert check_element1.is_displayed(), "Login blank message not displayed"
    
if __name__ == "__main__":
    pytest.main()