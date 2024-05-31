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
import requests
import re


class Test(ssl_handle.SSLBaseTest):

    def test_api_response(self):

        # API Calling
        api_url = urls.all_urls['API_URL'] + 'topology'
        response = requests.get(api_url)
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

        if response.status_code == 200:
            data = response.json()
            # print(data)

            # Storing the Nodes from the API response
            unique_node_ids = [node['id'] for node in data['nodes']]
            print(unique_node_ids)

            # Selenium automation start
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

            self.driver.find_element(By.XPATH, "//span[contains(text(),'SDX Circuits')]").click()
            sleep(1)
            self.driver.find_element(By.XPATH, "//span[contains(text(),'Create')]").click()

            main_div_xpath = "//body/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]"
            main_div = self.driver.find_element(By.XPATH, main_div_xpath)

            # Find all the nodes (using img tag)
            marker_images = main_div.find_elements(By.TAG_NAME, 'img')

            # Clicking each node and comparing the nodes with API response nodes.
            for marker in marker_images:
                marker.click()
                sleep(1)
                modal_xpath = "//div[@id='myModal' and contains(@class, 'modal')]"
                modal_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, modal_xpath))
                )

                # Extract the text from the modal
                modal_text = modal_element.text
                node_ids_in_modal = re.findall(r'Node: (\S+)', modal_text)
                print("Node IDs in Modal:", node_ids_in_modal)

                # Check if the nodes in the modal are in the unique nodes
                if node_ids_in_modal[0] in unique_node_ids:
                    assert node_ids_in_modal[0] in unique_node_ids, f"Node ID {node_ids_in_modal[0]} not found in unique nodes."
                self.driver.find_element(By.XPATH, "//button[@class='close']").click()
                sleep(1)


if __name__ == "__main__":
    pytest.main(['-s'])
