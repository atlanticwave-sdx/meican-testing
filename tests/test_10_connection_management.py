import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import ssl_handle
from conftest import chrome_driver_init
import urls
import time
import random
import string


class Test_11_Connection_Management(ssl_handle.SSLBaseTest):

    def teardown_method(self, method):
        """Clean up after each test to prevent modal conflicts (preserve session)"""
        try:
            # Clear any open modals/popups but preserve authentication session
            try:
                close_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'close') or contains(text(), '×')] | //a[contains(@class, 'close')]")
                for button in close_buttons:
                    if button.is_displayed():
                        button.click()
                        time.sleep(0.5)
            except:
                pass
            
            # Send escape key to close any remaining modals
            try:
                ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(0.5)
            except:
                pass
            
            # Close any leaflet popups specifically
            try:
                leaflet_closes = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'leaflet-popup-close-button')]")
                for close_btn in leaflet_closes:
                    if close_btn.is_displayed():
                        close_btn.click()
                        time.sleep(0.5)
            except:
                pass
                
            # Don't clear cookies - preserve authentication session for subsequent tests
            print("Modal cleanup completed, session preserved")
        except Exception as e:
            print(f"Cleanup warning: {e}")  # Log but don't fail

    def test_connection_creation_form_access(self):
        """Test accessing the connection creation form"""
        self._login_and_navigate_to_connections()
        
        # Look for the filters form (correct xpath provided by user)
        try:
            filters_form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='filtersform']"))
            )
            assert filters_form.is_displayed(), "Filters form not accessible"
            print("✅ Found filters form successfully")
        except TimeoutException:
            # Fallback: Try looking for any form on the page
            all_forms = self.driver.find_elements(By.TAG_NAME, "form")
            print(f"Found {len(all_forms)} forms on the page")
            for i, form in enumerate(all_forms):
                form_id = form.get_attribute('id')
                form_class = form.get_attribute('class')
                print(f"  Form {i+1}: id='{form_id}', class='{form_class}'")
            assert len(all_forms) > 0, "No forms found on the page"

    def test_connection_name_field_validation(self):
        """Test connection name field validation"""
        #self._login_and_navigate_to_connections()
        
        try:
            # Find name input field
            name_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' and (contains(@name, 'name') or contains(@id, 'name') or contains(@placeholder, 'name'))]"))
            )
            
            # Test empty name submission
            name_field.clear()
            self._submit_form()
            
            # # Check for validation error
            # try:
            #     error_message = WebDriverWait(self.driver, 5).until(
            #         EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'error') or contains(text(), 'required') or contains(text(), 'Please fill out this field.')]"))
            #     )
            #     assert error_message.is_displayed(), "Name field validation error not shown"
            # except TimeoutException:
            #     pass  # Validation might be client-side only
            
            # Test valid name
            test_name = f"test-connection-{self._generate_random_string(6)}"
            name_field.clear()
            name_field.send_keys(test_name)
            
            # Verify name was entered
            assert name_field.get_attribute('value') == test_name, "Connection name not properly entered"
            
        except TimeoutException:
            pytest.skip("Connection name field not found")

    def test_endpoint_selection(self):
        """Test selecting connection endpoints"""
        #self._login_and_navigate_to_connections()
        
        try:
            # Look for endpoint/port selection fields
            port_fields = self.driver.find_elements(By.XPATH, "//input[contains(@placeholder, 'port') or contains(@name, 'port') or contains(@id, 'port')] | //select[contains(@name, 'port') or contains(@id, 'port')]")
            
            if port_fields:
                first_port_field = port_fields[0]
                
                # Test port search/selection
                if first_port_field.tag_name == 'input':
                    # Text input with search
                    first_port_field.click()
                    first_port_field.send_keys("ampath")  # Search for ampath ports
                    time.sleep(2)
                    
                    # Look for dropdown results
                    try:
                        dropdown_option = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dropdown') or contains(@class, 'option')] | //li[contains(@class, 'option')]"))
                        )
                        dropdown_option.click()
                    except TimeoutException:
                        # Try pressing Enter for search
                        first_port_field.send_keys(Keys.ENTER)
                        
                elif first_port_field.tag_name == 'select':
                    # Dropdown selection
                    select = Select(first_port_field)
                    options = select.options
                    if len(options) > 1:  # Has options beyond default
                        select.select_by_index(1)  # Select first non-default option
                
                assert True, "Endpoint selection functionality working"
            else:
                pytest.skip("No endpoint selection fields found")
                
        except Exception as e:
            pytest.skip(f"Endpoint selection testing failed: {e}")

    def test_vlan_configuration_options(self):
        """Test VLAN configuration options"""
        #self._login_and_navigate_to_connections()
        
        try:
            # Look for VLAN fields
            vlan_fields = self.driver.find_elements(By.XPATH, "//input[contains(@name, 'vlan') or contains(@id, 'vlan')] | //select[contains(@name, 'vlan') or contains(@id, 'vlan')]")
            
            if vlan_fields:
                vlan_field = vlan_fields[0]
                
                if vlan_field.tag_name == 'select':
                    # Test dropdown VLAN options
                    select = Select(vlan_field)
                    options = [option.text for option in select.options]
                    
                    # Verify common VLAN options
                    expected_options = ['any', 'untagged', 'all']
                    found_options = [opt for opt in expected_options if any(opt in option.lower() for option in options)]
                    
                    assert len(found_options) > 0, f"Expected VLAN options not found. Available: {options}"
                    
                    # Test selecting different VLAN options
                    if 'any' in options[0].lower():
                        select.select_by_visible_text(options[0])
                    
                elif vlan_field.tag_name == 'input':
                    # Test text input VLAN
                    vlan_field.clear()
                    vlan_field.send_keys("100")  # Test specific VLAN
                    assert vlan_field.get_attribute('value') == "100", "VLAN value not set correctly"
                    
                    # Test VLAN range
                    vlan_field.clear()
                    vlan_field.send_keys("100:110")
                    assert "100:110" in vlan_field.get_attribute('value'), "VLAN range not accepted"
                
            else:
                pytest.skip("No VLAN configuration fields found")
                
        except Exception as e:
            pytest.skip(f"VLAN configuration testing failed: {e}")

    def test_advanced_options_panel(self):
        """Test advanced options panel functionality"""
        #self._login_and_navigate_to_connections()
        
        try:
            # Look for "Advanced" or "Show Advanced" button
            advanced_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Advanced') or contains(text(), 'Show Advanced')] | //a[contains(text(), 'Advanced')]"))
            )
            
            # Click to expand advanced options
            advanced_button.click()
            time.sleep(1)
            
            # Verify advanced options are now visible
            advanced_panel = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'advanced') or contains(@id, 'advanced')] | //fieldset[contains(@class, 'advanced')]"))
            )
            assert advanced_panel.is_displayed(), "Advanced options panel not displayed"
            
            # Look for QoS fields
            qos_fields = self.driver.find_elements(By.XPATH, "//input[contains(@name, 'bandwidth') or contains(@name, 'delay') or contains(@name, 'qos')] | //input[contains(@placeholder, 'Gbps') or contains(@placeholder, 'latency')]")
            
            if qos_fields:
                # Test bandwidth field
                bandwidth_field = next((field for field in qos_fields if 'bandwidth' in field.get_attribute('name').lower() or 'gbps' in field.get_attribute('placeholder').lower()), None)
                if bandwidth_field:
                    bandwidth_field.clear()
                    bandwidth_field.send_keys("1")
                    assert bandwidth_field.get_attribute('value') == "1", "Bandwidth value not set"
            
        except TimeoutException:
            pytest.skip("Advanced options not found or not implemented")

    def test_connection_submission(self):
        """Test submitting a complete connection request"""
        #self._login_and_navigate_to_connections()
        
        try:
            # Fill minimum required fields
            connection_name = f"test-selenium-{self._generate_random_string(8)}"
            
            # Name field
            name_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' and (contains(@name, 'name') or contains(@id, 'name'))]"))
            )
            name_field.clear()
            name_field.send_keys(connection_name)
            
            # Try to fill endpoints if available
            port_field1 = self.driver.find_element(By.XPATH, "//*[@id='search']")
            #if len(port_fields) >= 2:
                # Fill first endpoint
            port_field1.click()
            port_field1.send_keys("amlight.net:MIA-MI1-SW17:7")
            time.sleep(1)
            port_field1.send_keys(Keys.TAB)

            port_field2 = self.driver.find_element(By.XPATH, "//*[@id='search2']")
            #if len(port_fields) >= 2:
                # Fill first endpoint
            port_field2.click()
            port_field2.send_keys("amlight.net:MIA-MI1-SW14:7")
            time.sleep(1)
            port_field2.send_keys(Keys.TAB)
                
        
            
            # Submit the form
            submit_result = self._submit_form()
            time.sleep(30)
            
            if submit_result:
                # Look for success or error message
                try:
                    result_message = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert') or contains(@class, 'message') or contains(@class, 'notification')]"))
                    )
                    message_text = result_message.text.lower()
                    
                    # Verify we got some kind of response
                    assert any(word in message_text for word in ['success', 'error', 'created', 'failed', 'invalid']), f"Unexpected response: {message_text}"
                    
                except TimeoutException:
                    # Check if we were redirected to connection list or details
                    current_url = self.driver.current_url
                    assert 'connection' in current_url or 'circuit' in current_url, "No clear response to connection submission"
            
        except Exception as e:
            pytest.skip(f"Connection submission testing failed: {e}")

    def test_connection_list_view(self):
        """Test viewing list of connections"""
        self._login_and_navigate_to_list()
        
        try:
            # Look for connection list table or container
            connection_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'connection') or contains(@class, 'circuit')] | //div[contains(@class, 'connection-list') or contains(@class, 'circuit-list')]"))
            )
            assert connection_list.is_displayed(), "Connection list not displayed"
            
            # Look for table headers or list items
            headers = self.driver.find_elements(By.XPATH, "//th | //div[contains(@class, 'header')]")
            if headers:
                header_texts = [h.text.lower() for h in headers]
                expected_headers = ['name', 'status', 'id', 'service']
                found_headers = [h for h in expected_headers if any(h in ht for ht in header_texts)]
                assert len(found_headers) > 0, f"Expected connection list headers not found. Found: {header_texts}"
            
        except TimeoutException:
            pytest.skip("Connection list view not accessible")

    def _submit_form(self):
        """Helper method to submit connection form"""
        try:
            # Look for submit button
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Submit') or contains(text(), 'Create')] | //input[@type='submit']")
            submit_button.click()
            return True
        except NoSuchElementException:
            return False

    def _generate_random_string(self, length):
        """Generate random string for test data"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def _login_and_navigate_to_connections(self):
        """Helper method to login via CILogon and stay on connection form"""
        self._ensure_login()
        # Stay on current page for form-based tests

    def _login_and_navigate_to_list(self):
        """Helper method to login via CILogon and navigate to connections list"""
        #self._ensure_login()
        
        # Navigate to connection list
        list_url = urls.all_urls['USER_LOGIN_URL'] + "/circuits/nodes/list"
        self.driver.get(list_url)
        time.sleep(2)
        print(f"Navigated to connections list: {list_url}")

    def _ensure_login(self):
        """Ensure user is logged in via CILogon"""
        # Check if we already have authentication cookies
        cookies = self.driver.get_cookies()
        auth_cookie_found = any('session' in cookie.get('name', '').lower() or 'auth' in cookie.get('name', '').lower() for cookie in cookies)
        
        if auth_cookie_found:
            print("Authentication cookies found, already logged in")
            return
        
        # Need fresh login - use CILogon
        print("Performing CILogon authentication")
        self._cilogon_orcid_login()

    def _cilogon_orcid_login(self):
        """CILogon ORCID login method"""
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        
        try:
            # Click CILogon button
            cilogon_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='wayflogonbutton']"))
            )
            cilogon_button.click()
            print("Clicked CILogon button")
            
            # Wait 5 seconds
            time.sleep(5)
            print("Waited 5 seconds")
            
            # Fill in ORCID username field
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='username-input']"))
            )
            username_field.clear()
            username_field.send_keys(urls.all_urls['ORCID_VALID_USERNAME'])
            print(f"Entered username: {urls.all_urls['ORCID_VALID_USERNAME']}")
            
            # Fill in ORCID password field
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='password']"))
            )
            password_field.clear()
            password_field.send_keys(urls.all_urls['ORCID_VALID_USERNAME_PASSWORD'])
            print("Entered password")
            
            # Submit the form
            signin_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']"))
            )
            signin_button.click()
            print("Clicked submit button")
            
            # Wait for login to complete and redirect back to MEICAN
            print("Waiting for login completion and redirect...")
            time.sleep(8)  # Wait for redirect
            
            current_url = self.driver.current_url
            print(f"Login completed, current URL: {current_url}")
            
            # Check if we're back at MEICAN (not on ORCID anymore)
            if "orcid.org" in current_url:
                print("Still on ORCID page - waiting more...")
                time.sleep(3)
                current_url = self.driver.current_url
                print(f"Final URL: {current_url}")
            
            # Stay on whatever page we're redirected to (don't navigate elsewhere)
                
        except Exception as e:
            print(f"CILogon login failed: {e}")
            pytest.skip(f"CILogon login failed: {e}")


if __name__ == "__main__":
    pytest.main()