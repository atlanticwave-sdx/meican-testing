import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
import ssl_handle
import cookies_handle
from conftest import chrome_driver_init
import urls
from time import sleep

class Test(ssl_handle.SSLBaseTest, cookies_handle.CookiesBaseTest):

    # Entering wrong credentials for login password fields and clicking sign in
    def test_user_login_all_wrong_credentials(self):
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        self.handle_cookies_warning(urls.all_urls['USER_LOGIN_URL'])

        self.driver.find_element(By.ID, "username-input").send_keys("0000-0000-0000-0000")
        self.driver.find_element(By.ID, "password").send_keys("Password11wdfg")
        self.driver.find_element(By.ID, "signin-button").click()

        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "dialogTitle"))
        )
        assert check_element.is_displayed(), "Something's not quite right... message not displayed"

    # Entering blank credentials for login password fields and clicking sign in
    def test_user_login_all_blank_credentials(self):
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        self.handle_cookies_warning(urls.all_urls['USER_LOGIN_URL'])

        self.driver.find_element(By.ID, "signin-button").click()

        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//mat-error[contains(., 'Please enter your email address or your ORCID iD')]"))
        )
        assert check_element.is_displayed(), "Please enter your email address or your ORCID iD message not displayed"

    # Entering blank login invalid password fields and clicking sign in
    def test_user_login_blank_login_invalid_password(self):
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        self.handle_cookies_warning(urls.all_urls['USER_LOGIN_URL'])

        self.driver.find_element(By.ID, "password").send_keys("Password11")
        self.driver.find_element(By.ID, "signin-button").click()

        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//mat-error[contains(., 'Please enter your email address or your ORCID iD')]"))
        )
        assert check_element.is_displayed(), "Please enter your email address or your ORCID iD message not displayed"

    # Entering blank password wrong login and clicking sign in
    def test_user_login_blank_password_wrong_login(self):
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        self.handle_cookies_warning(urls.all_urls['USER_LOGIN_URL'])

        self.driver.find_element(By.ID, "username-input").send_keys("0000-0000-0000-0000")
        self.driver.find_element(By.ID, "signin-button").click()

        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "dialogTitle"))
        )
        assert check_element.is_displayed(), "Something's not quite right... message not displayed"

    # Entering blank login valid password fields and clicking sign in
    def test_user_login_blank_login_valid_password(self):
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        self.handle_cookies_warning(urls.all_urls['USER_LOGIN_URL'])

        self.driver.find_element(By.ID, "password").send_keys("qazwsxedc123@123")
        self.driver.find_element(By.ID, "signin-button").click()

        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//mat-error[contains(., 'Please enter your email address or your ORCID iD')]"))
        )
        assert check_element.is_displayed(), "Please enter your email address or your ORCID iD message not displayed"

    # Entering blank password valid login and clicking sign in
    def test_user_login_blank_password_valid_login(self):
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        self.handle_cookies_warning(urls.all_urls['USER_LOGIN_URL'])

        self.driver.find_element(By.ID, "username-input").send_keys("0009-0002-3398-6622")
        self.driver.find_element(By.ID, "signin-button").click()

        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "dialogTitle"))
        )
        assert check_element.is_displayed(), "Something's not quite right.. message not displayed"

    # Entering invalid login format and clicking sign in
    def test_user_login_invalid_login_format(self):
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        self.handle_cookies_warning(urls.all_urls['USER_LOGIN_URL'])

        self.driver.find_element(By.ID, "username-input").send_keys("invalid_format")
        self.driver.find_element(By.ID, "signin-button").click()

        check_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//mat-error[contains(., 'Please enter a valid email address or ORCID iD')]"))
        )
        assert check_element.is_displayed(), "Please enter a valid email address or ORCID iD message displayed"

    # Entering valid login password fields and clicking sign in
    def test_user_login_all_valid_credentials(self):
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        self.handle_cookies_warning(urls.all_urls['USER_LOGIN_URL'])

        self.driver.find_element(By.ID, "username-input").send_keys(urls.all_urls['ORCID_VALID_USERNAME'])
        self.driver.find_element(By.ID, "password").send_keys(urls.all_urls['ORCID_VALID_USERNAME_PASSWORD'])
        self.driver.find_element(By.ID, "signin-button").click()

        check_element1 = None
        check_element2 = None

        try:
            # Try to locate the first element (email sent to verify)
            check_element1 = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(text(),'We sent you an email to confirm your account. please complete verification.')]"))
            )
        except TimeoutException:
            # If the first element is not found, try to locate the second element (verifying for the first time)
            try:
                check_element2 = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//p[contains(text(),'Verify your Email')]"))
                )
            except TimeoutException:
                pass

        if check_element1 is not None and check_element1.is_displayed():
            is_displayed = True
            sleep(1)
        elif check_element2 is not None and check_element2.is_displayed():
            is_displayed = True
            self.perform_blank_email_test()
            self.perform_invalid_email_test()
            self.perform_valid_email_test()
        else:
            is_displayed = False

        assert is_displayed, "User is not able to login via Orcid"

    # Below 3 tests are for meican verification
    def perform_blank_email_test(self):
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
        sleep(1)

        active_element = self.driver.switch_to.active_element
        message_text = active_element.get_attribute("validationMessage")
        assert message_text == "Please fill out this field.", "Validation message does not match."

    def perform_invalid_email_test(self):
        self.driver.find_element(By.XPATH, "//input[@id='loginform-login']").send_keys("invalid_email")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()

        sleep(1)
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        expected_text = "Email is not a valid email address."
        assert alert_text == expected_text, f"Alert text does not match. Expected: {expected_text}, Got: {alert_text}"
        alert.accept()

    def perform_valid_email_test(self):
        self.driver.find_element(By.XPATH, "//input[@id='loginform-login']").send_keys(urls.all_urls['ORCID_USER_EMAIL'])
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()

        sleep(1)
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        expected_text = "Email Sent successfully"
        assert alert_text == expected_text, f"Alert text does not match. Expected: {expected_text}, Got: {alert_text}"
        alert.accept()


if __name__ == "__main__":
    pytest.main()