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
from time import sleep
from selenium.webdriver.support.ui import Select


class Test(ssl_handle.SSLBaseTest):

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

        self.driver.find_element(By.XPATH, "//li/a/span[text()='Users']").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//li/ul/li[1]/a/span[text()='Users']").click()
        sleep(1)

        # Locating the row containing the user with the name "Selenium Testing User"
        user_row = 0
        try:
            user_row = self.driver.find_element(
                By.XPATH,
                "//tbody/tr[td[contains(text(), 'Selenium Testing User')]]"
            )
        except NoSuchElementException:
            print("Selenium Testing User is not created")

        # Locating the edit/view element within the user row and click it
        if user_row:
            eye_icon = user_row.find_element(By.XPATH, "td[2]/a/span[contains(@class, 'fa fa-eye')]")
            eye_icon.click()
            sleep(1)

            empty_div = 0
            try:
                user_row = self.driver.find_element(
                    By.XPATH,
                    "//tbody/tr/td/div[@class='empty' and text()='No results found.']]"
                )
            except NoSuchElementException:
                print("No results found not present")

            # empty_div = WebDriverWait(self.driver, 10).until(
            #     EC.visibility_of_element_located((By.XPATH, "//tbody/tr/td/div[@class='empty' and text()='No results found.']"))
            # )

            if empty_div:
                self.driver.find_element(By.XPATH, "//a[text()='Add']").click()
                sleep(1)
                dropdown_element = self.driver.find_element(By.ID, "userdomainrole-_grouprolename")
                dropdown = Select(dropdown_element)
                dropdown.select_by_visible_text("SDX Circuit")
                sleep(1)
                self.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()

                check_element2 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Role created successfully')]"))
                )
                # // span[contains(text(), 'The user already has this profile')]
                assert check_element2.is_displayed(), "Role created successfully message not displayed"
            else:
                table_body = self.driver.find_element(By.XPATH, "//tbody")
                rows = table_body.find_elements(By.TAG_NAME, "tr")
                SDX_circuit_found = 0

                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 3:  # Ensure there are at least 3 cells in the row
                        group_name = cells[2].text
                        if group_name == "SDX Circuit":
                            SDX_circuit_found = 1
                            break
                if SDX_circuit_found == 0:
                    self.driver.find_element(By.XPATH, "//a[text()='Add']").click()
                    sleep(1)
                    dropdown_element = self.driver.find_element(By.ID, "userdomainrole-_grouprolename")
                    dropdown = Select(dropdown_element)
                    dropdown.select_by_visible_text("SDX Circuit")
                    sleep(1)
                    self.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
                    sleep(1)

                    check_element2 = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Role created successfully')]"))
                    )
                    assert check_element2.is_displayed(), "Role created successfully message not displayed"


if __name__ == "__main__":
    pytest.main()