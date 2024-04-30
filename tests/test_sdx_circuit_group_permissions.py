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


class Test(ssl_handle.SSLBaseTest):

    def test(self):
        self.handle_ssl_warning(urls.all_urls['ADMIN_LOGIN_URL'])

        login = "master"
        password = "master"

        self.driver.find_element(By.ID, "loginform-login").send_keys(login)
        self.driver.find_element(By.ID, "loginform-password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

        check_element1 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Dashboard')]"))
        )
        assert check_element1.is_displayed(), "Dashboard element not visible after login"

        # Read check
        self.driver.find_element(By.XPATH, "//li/a/span[text()='Users']").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//span[contains(text(),'Groups')]").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//tbody/tr[10]/td[2]/a[1]/span[1]").click()
        sleep(1)

        self.driver.find_element(By.XPATH, "//tbody/tr[7]/td[3]/div[1]/ins[1]").click()
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
        sleep(1)
        check_element2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Group updated successfully')]"))
        )
        assert check_element2.is_displayed(), "Group updated successfully message not displayed"
        sleep(1)
        self.driver.find_element(By.XPATH, "//a/span[text()='SDX Circuits']").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//a/span[text()='SDX Circuits']").click()
        view_link = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//body/div[1]/aside[1]/section[1]/ul[1]/li[3]/ul[1]/li[2]/a[1]"))
        )

        assert view_link.is_displayed(), "View button is not displayed under SDX Circuits"


        # Update check
        self.driver.find_element(By.XPATH, "//li/a/span[text()='Users']").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//span[contains(text(),'Groups')]").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//tbody/tr[10]/td[2]/a[1]/span[1]").click()
        sleep(1)

        self.driver.find_element(By.XPATH, "//tbody/tr[7]/td[4]/div[1]/ins[1]").click()
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
        sleep(1)
        check_element3 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Group updated successfully')]"))
        )
        assert check_element3.is_displayed(), "Group updated successfully message not displayed"
        sleep(1)
        self.driver.find_element(By.XPATH, "//a/span[text()='SDX Circuits']").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//a/span[text()='SDX Circuits']").click()

        update_link = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'Update')]"))
        )
        assert update_link.is_displayed(), "Update button is not displayed under SDX Circuits"


        # Delete check
        self.driver.find_element(By.XPATH, "//li/a/span[text()='Users']").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//span[contains(text(),'Groups')]").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//tbody/tr[10]/td[2]/a[1]/span[1]").click()
        sleep(1)

        self.driver.find_element(By.XPATH, "//tbody/tr[7]/td[5]/div[1]/ins[1]").click()
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
        sleep(1)
        check_element4 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Group updated successfully')]"))
        )
        assert check_element4.is_displayed(), "Group updated successfully message not displayed"
        sleep(1)
        self.driver.find_element(By.XPATH, "//a/span[text()='SDX Circuits']").click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//a/span[text()='SDX Circuits']").click()

        delete_link = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'Delete')]"))
        )
        assert delete_link.is_displayed(), "Delete button is not displayed under SDX Circuits"

if __name__ == "__main__":
    pytest.main()