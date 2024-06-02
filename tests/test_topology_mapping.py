import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import ssl_handle
from conftest import chrome_driver_init
import urls
from time import sleep
import requests
import re


class Test(ssl_handle.SSLBaseTest):

    def test_api_response(self):
        try:
            # API Calling
            api_url = urls.all_urls['API_URL'] + 'topology'
            response = requests.get(api_url)
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

            if response.status_code == 200:
                data = response.json()

                # # Storing the Nodes from the API response in a dictionary with initial value as False
                # api_url_node_ids = {node['id']: True for node in data['nodes']}
                # print(f'\nThe nodes from the API are - \n{list(api_url_node_ids.values())} \n')
                api_url_node_ids = [node['id'] for node in data['nodes']]
                print(f'\n \nThe nodes from the API are - \n{api_url_node_ids}')
                # api_url_node_ids = []

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

                # Finding all the nodes (using img tag)
                marker_images = main_div.find_elements(By.TAG_NAME, 'img')

                # Clicking each node and comparing the nodes with API response nodes.
                ui_node_ids = []
                count = 1
                for marker in marker_images:
                    try:
                        marker.click()
                    except ElementClickInterceptedException:
                        self.driver.execute_script("arguments[0].click();", marker)

                    sleep(1)
                    print(f"\nNode - {count}")

                    modal_xpath = "//div[@id='myModal' and contains(@class, 'modal')]"
                    modal_element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, modal_xpath))
                    )

                    modal_text = modal_element.text
                    location = re.findall(r'Location: (\S+)', modal_text)
                    print(f"Locations at this node are - {location}")

                    location_sections = modal_text.split("Location:")
                    for section in location_sections[1:]:
                        lines = section.split('\n')
                        location = lines[0].strip()
                        for line in lines:
                            node_match = re.search(r'Node: (\S+)', line)
                            if node_match:
                                node_id = node_match.group(1)
                                ui_node_ids.append(node_id)
                                status = "Found in API URL" if node_id in api_url_node_ids else "Not Found in API URL"
                                print(f'Location: {location}, Node: {node_id}, Status: {status}')

                    self.driver.find_element(By.XPATH, "//button[@class='close']").click()
                    sleep(1)
                    count += 1

                # print(f'\nThe nodes from the UI are - \n{ui_node_ids}')
                # missing_nodes = [node for node, found in api_url_node_ids.items() if not found]
                # assert not missing_nodes, f"The following nodes were not found in the UI: {missing_nodes}"

        except TimeoutException as e:
            print(f"TimeoutException: {str(e)}")
            assert False, "A timeout occurred during the test execution."


if __name__ == "__main__":
    pytest.main(['-s'])
