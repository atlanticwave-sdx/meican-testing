import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from tests.Pre_Test_Checks.ssl_handle import SSLBaseTest
from tests.Web_Driver.conftest import chrome_driver_init
from tests.URLS.urls import all_urls

class Test_1(SSLBaseTest):

    # Entering wrong credentials for login and pasword fields and clicking sign in
    def test_wrong_credentials(self):
        self.handle_ssl_warning(all_urls['ADMIN_LOGIN_URL'])
        
        login = "wrong_credentials"
        password = "wrong_credentials"
            
        self.driver.find_element(By.ID, "loginform-login").send_keys(login)
        self.driver.find_element(By.ID, "loginform-password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[text()='Sign in']").click()
        
        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Incorrect username or password.')]"))
        )
        assert check_element.is_displayed(), "Incorrect username or password message not displayed"
    
if __name__ == "__main__":
    pytest.main()