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

    def test_topology_mapping(self):
        try:
            # API Calling
            api_url = urls.all_urls['API_URL'] + 'topology'
            response = requests.get(api_url)
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

            if response.status_code == 200:
                data = response.json()

                api_url_node_ids = [node['id'] for node in data['nodes']]
                api_url_node_ids.append("test_id")
                api_url_node_ids.append("test_id12")
                api_url_node_ids.append('urn:sdx:node:ampath.net:Ampath12')
                print(f'\n \nThe nodes from the API are - \n{api_url_node_ids}\n')

                node_status_dict = {node['id']: {
                    "location": node.get('location', {}).get('address', 'Unknown Location'),
                    "found": False} for node in data['nodes']}

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

                # Clicking each node and extracting the node details.
                ui_node_ids = []
                for marker in marker_images:
                    try:
                        marker.click()
                    except ElementClickInterceptedException:
                        self.driver.execute_script("arguments[0].click();", marker)
                    sleep(1)

                    modal_xpath = "//div[@id='myModal' and contains(@class, 'modal')]"
                    modal_element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, modal_xpath))
                    )

                    modal_text = modal_element.text
                    location_sections = modal_text.split("Location:")
                    for section in location_sections[1:]:
                        lines = section.split('\n')
                        for line in lines:
                            node_match = re.search(r'Node: (\S+)', line)
                            if node_match:
                                node_id = node_match.group(1)
                                ui_node_ids.append(node_id)

                    self.driver.find_element(By.XPATH, "//button[@class='close']").click()
                    sleep(1)

                # Checking if API nodes are in UI nodes
                # not_found_nodes = []
                dict_array = {}
                for api_node_id in api_url_node_ids:
                    status = "True" if api_node_id in ui_node_ids else "False"
                    # location_address = node_status_dict.get(api_node_id, {}).get('location', 'Unknown Location')
                    #
                    # if api_node_id in node_status_dict:
                    #     node_status_dict[api_node_id]["found"] = True if status == "Found in UI" else False
                    # else:
                    #     not_found_nodes.append(api_node_id)
                    #
                    # print(f'Location: {location_address}, Node: {api_node_id}, Status: {status}')
                    dict_array[api_node_id] = status
                print(f"The dict array is - {dict_array}")

                # print("\nNodes not found in the UI:")
                # for node_id in not_found_nodes:
                #     print(node_id)

                if "False" in dict_array.values():
                    assert False, f"Not all nodes were found in the UI."

                # all_found = all(details["found"] for details in node_status_dict.values())
                # assert all_found, f"Not all nodes were found in the UI. Details: {node_status_dict}"

        except TimeoutException as e:
            print(f"TimeoutException: {str(e)}")
            assert False, "A timeout occurred during the test execution."


if __name__ == "__main__":
    pytest.main()
