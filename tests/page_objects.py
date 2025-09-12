"""
Page Object Model for MEICAN SDX UI testing
This module contains page objects to improve test maintainability and reduce code duplication
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def handle_ssl_warning(self, url):
        """Handle SSL warning if present"""
        self.driver.get(url)
        try:
            ssl_warning = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Your connection is not private')]")
            if ssl_warning:
                self.driver.find_element(By.ID, "details-button").click()
                self.driver.find_element(By.ID, "proceed-link").click()
        except NoSuchElementException:
            pass
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to finish loading"""
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")


class LoginPage(BasePage):
    """Page object for login functionality"""
    
    # Locators
    ADMIN_LOGIN_FIELD = (By.ID, "loginform-login")
    ADMIN_PASSWORD_FIELD = (By.ID, "loginform-password")
    ADMIN_SIGNIN_BUTTON = (By.XPATH, "//button[text()='Sign in']")
    ORCID_LOGIN_LINK = (By.XPATH, "//a[contains(@href, 'orcid') or contains(text(), 'ORCID')]")
    CILOGON_LOGIN_LINK = (By.XPATH, "//a[contains(@href, 'cilogon') or contains(text(), 'CILogon')]")
    DASHBOARD_ELEMENT = (By.XPATH, "//span[contains(text(),'Dashboard')]")
    
    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
    
    def load_admin_login(self):
        """Load admin login page"""
        self.handle_ssl_warning(f"{self.base_url}/aaa/login/admin")
    
    def load_user_login(self):
        """Load user login page"""
        self.handle_ssl_warning(self.base_url)
    
    def admin_login(self, username, password):
        """Perform admin login"""
        self.load_admin_login()
        self.wait.until(EC.presence_of_element_located(self.ADMIN_LOGIN_FIELD)).send_keys(username)
        self.driver.find_element(*self.ADMIN_PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.ADMIN_SIGNIN_BUTTON).click()
        
        # Wait for successful login
        self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_ELEMENT))
        return True
    
    def click_orcid_login(self):
        """Click ORCID login option"""
        self.load_user_login()
        orcid_element = self.wait.until(EC.element_to_be_clickable(self.ORCID_LOGIN_LINK))
        orcid_element.click()
        return True
    
    def click_cilogon_login(self):
        """Click CILogon login option"""
        self.load_user_login()
        cilogon_element = self.wait.until(EC.element_to_be_clickable(self.CILOGON_LOGIN_LINK))
        cilogon_element.click()
        return True
    
    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            self.driver.find_element(*self.DASHBOARD_ELEMENT)
            return True
        except NoSuchElementException:
            return False


class TopologyPage(BasePage):
    """Page object for topology visualization"""
    
    # Locators
    MAP_CONTAINER = (By.XPATH, "//div[contains(@id, 'map') or contains(@class, 'map') or contains(@id, 'topology')]")
    NODE_MARKERS = (By.XPATH, "//img[contains(@class, 'leaflet-marker-icon') and contains(@class, 'leaflet-zoom-animated') and contains(@class, 'leaflet-interactive')]")
    AUTO_REFRESH_TOGGLE = (By.XPATH, "//*[@id='autoRefreshToggle']")
    SEARCH_FIELD = (By.XPATH, "//input[@type='text' and (contains(@placeholder, 'search') or contains(@id, 'search'))]")
    
    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
    
    def load_topology(self):
        """Load topology visualization page"""
        self.driver.get(f"{self.base_url}/circuits/nodes/show")
        self.wait_for_topology_load()
    
    def wait_for_topology_load(self):
        """Wait for topology map to load"""
        self.wait.until(EC.presence_of_element_located(self.MAP_CONTAINER))
        time.sleep(3)  # Allow map rendering
    
    def get_visible_nodes(self):
        """Get list of visible node elements"""
        try:
            return self.driver.find_elements(*self.NODE_MARKERS)
        except NoSuchElementException:
            return []
    
    def click_node(self, node_index=0):
        """Click on a network node"""
        nodes = self.get_visible_nodes()
        if nodes and len(nodes) > node_index:
            ActionChains(self.driver).move_to_element(nodes[node_index]).click().perform()
            return True
        return False
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        try:
            toggle = self.wait.until(EC.element_to_be_clickable(self.AUTO_REFRESH_TOGGLE))
            initial_state = toggle.is_selected() if toggle.tag_name == 'input' else toggle.is_enabled()
            toggle.click()
            time.sleep(1)
            new_state = toggle.is_selected() if toggle.tag_name == 'input' else toggle.is_enabled()
            return initial_state != new_state
        except TimeoutException:
            return False
    
    def search_nodes(self, search_term):
        """Search for nodes on the topology"""
        try:
            search_field = self.wait.until(EC.presence_of_element_located(self.SEARCH_FIELD))
            search_field.clear()
            search_field.send_keys(search_term)
            search_field.send_keys(Keys.ENTER)
            time.sleep(2)
            return True
        except TimeoutException:
            return False


class ConnectionPage(BasePage):
    """Page object for connection management"""
    
    # Locators
    CONNECTION_FORM = (By.XPATH, "//form[contains(@class, 'connection') or contains(@id, 'connection')]")
    NAME_FIELD = (By.XPATH, "//input[@type='text' and (contains(@name, 'name') or contains(@id, 'name'))]")
    PORT_FIELDS = (By.XPATH, "//input[contains(@placeholder, 'port') or contains(@name, 'port')] | //select[contains(@name, 'port')]")
    VLAN_FIELDS = (By.XPATH, "//input[contains(@name, 'vlan') or contains(@id, 'vlan')] | //select[contains(@name, 'vlan')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' or contains(text(), 'Submit') or contains(text(), 'Create')] | //input[@type='submit']")
    ADVANCED_OPTIONS_BUTTON = (By.XPATH, "//button[contains(text(), 'Advanced') or contains(text(), 'Show Advanced')]")
    BANDWIDTH_FIELD = (By.XPATH, "//input[contains(@name, 'bandwidth') or contains(@placeholder, 'Gbps')]")
    DELAY_FIELD = (By.XPATH, "//input[contains(@name, 'delay') or contains(@placeholder, 'latency')]")
    NOTIFICATION_FIELDS = (By.XPATH, "//input[contains(@name, 'email') or contains(@placeholder, 'email')]")
    
    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
    
    def load_connection_page(self):
        """Load connection creation page"""
        self.driver.get(f"{self.base_url}/circuits/nodes/show")
        self.wait_for_page_load()
    
    def load_connection_list(self):
        """Load connection list page"""
        self.driver.get(f"{self.base_url}/circuits/nodes/list")
        self.wait_for_page_load()
    
    def set_connection_name(self, name):
        """Set connection name"""
        name_field = self.wait.until(EC.presence_of_element_located(self.NAME_FIELD))
        name_field.clear()
        name_field.send_keys(name)
        return name_field.get_attribute('value') == name
    
    def set_endpoints(self, source_port, dest_port):
        """Set source and destination endpoints"""
        port_fields = self.driver.find_elements(*self.PORT_FIELDS)
        if len(port_fields) >= 2:
            # Set source port
            port_fields[0].click()
            port_fields[0].send_keys(source_port)
            time.sleep(1)
            port_fields[0].send_keys(Keys.TAB)
            
            # Set destination port
            port_fields[1].click()
            port_fields[1].send_keys(dest_port)
            time.sleep(1)
            port_fields[1].send_keys(Keys.TAB)
            return True
        return False
    
    def set_vlan_configuration(self, vlan_value, endpoint_index=0):
        """Set VLAN configuration for an endpoint"""
        vlan_fields = self.driver.find_elements(*self.VLAN_FIELDS)
        if len(vlan_fields) > endpoint_index:
            vlan_field = vlan_fields[endpoint_index]
            
            if vlan_field.tag_name == 'select':
                select = Select(vlan_field)
                try:
                    select.select_by_visible_text(vlan_value)
                except:
                    select.select_by_value(vlan_value)
            else:
                vlan_field.clear()
                vlan_field.send_keys(vlan_value)
            return True
        return False
    
    def expand_advanced_options(self):
        """Expand advanced options panel"""
        try:
            advanced_button = self.wait.until(EC.element_to_be_clickable(self.ADVANCED_OPTIONS_BUTTON))
            advanced_button.click()
            time.sleep(1)
            return True
        except TimeoutException:
            return False
    
    def set_bandwidth_requirement(self, bandwidth_gbps):
        """Set bandwidth requirement in Gbps"""
        try:
            bandwidth_field = self.wait.until(EC.presence_of_element_located(self.BANDWIDTH_FIELD))
            bandwidth_field.clear()
            bandwidth_field.send_keys(str(bandwidth_gbps))
            return True
        except TimeoutException:
            return False
    
    def set_latency_requirement(self, max_delay_ms):
        """Set maximum latency requirement in milliseconds"""
        try:
            delay_field = self.wait.until(EC.presence_of_element_located(self.DELAY_FIELD))
            delay_field.clear()
            delay_field.send_keys(str(max_delay_ms))
            return True
        except TimeoutException:
            return False
    
    def add_notification_email(self, email, field_index=0):
        """Add notification email address"""
        notification_fields = self.driver.find_elements(*self.NOTIFICATION_FIELDS)
        if len(notification_fields) > field_index:
            notification_fields[field_index].clear()
            notification_fields[field_index].send_keys(email)
            return True
        return False
    
    def submit_connection(self):
        """Submit connection creation form"""
        try:
            submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
            submit_button.click()
            return True
        except TimeoutException:
            return False
    
    def get_form_validation_errors(self):
        """Get any form validation error messages"""
        try:
            error_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'invalid')] | //span[contains(@class, 'error')]")
            return [elem.text for elem in error_elements if elem.is_displayed()]
        except:
            return []
    
    def get_success_message(self):
        """Get success message after form submission"""
        try:
            success_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'success') or contains(@class, 'alert-success')] | //span[contains(text(), 'success') or contains(text(), 'created')]")
            ))
            return success_element.text
        except TimeoutException:
            return None


class ORCIDPage(BasePage):
    """Page object for ORCID authentication"""
    
    # Locators
    USERNAME_FIELD = (By.XPATH, "//*[@id='username-input']")
    PASSWORD_FIELD = (By.XPATH, "//*[@id='password']")
    SIGNIN_BUTTON = (By.XPATH, "//button[@type='submit'] | //input[@type='submit']")
    AUTHORIZE_BUTTON = (By.XPATH, "//button[contains(text(), 'Authorize') or contains(text(), 'Continue')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'error')] | //span[contains(@class, 'error')]")
    
    def login_with_orcid(self, username, password):
        """Perform ORCID login"""
        # Wait for ORCID page to load
        self.wait.until(lambda driver: "orcid.org" in driver.current_url)
        
        # Enter credentials
        username_field = self.wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        # Submit login
        signin_button = self.driver.find_element(*self.SIGNIN_BUTTON)
        signin_button.click()
        
        # Handle authorization page if present
        try:
            authorize_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.AUTHORIZE_BUTTON)
            )
            authorize_button.click()
        except TimeoutException:
            pass  # No authorization page
        
        # Wait for redirect back to MEICAN
        self.wait.until(lambda driver: "orcid.org" not in driver.current_url)
        return True
    
    def get_login_error(self):
        """Get login error message"""
        try:
            error_element = self.wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
            return error_element.text
        except TimeoutException:
            return None


class CILogonPage(BasePage):
    """Page object for CILogon authentication"""
    
    # Locators
    INSTITUTION_DROPDOWN = (By.ID, "idp")
    CONTINUE_BUTTON = (By.XPATH, "//*[@id='wayflogonbutton']")
    COOKIES_ACCEPT_BUTTON = (By.XPATH, "//*[@id='onetrust-accept-btn-handler']")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'error')] | //span[contains(text(), 'select') or contains(text(), 'choose')]")
    
    def handle_cookies_popup(self):
        """Handle cookies acceptance popup if present"""
        try:
            cookies_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.COOKIES_ACCEPT_BUTTON)
            )
            cookies_button.click()
            return True
        except TimeoutException:
            return False
    
    def select_institution(self, institution_name):
        """Select institution from dropdown"""
        # Wait for CILogon page
        self.wait.until(lambda driver: "cilogon.org" in driver.current_url)
        
        # Handle cookies popup first
        self.handle_cookies_popup()
        
        institution_dropdown = self.wait.until(EC.presence_of_element_located(self.INSTITUTION_DROPDOWN))
        select = Select(institution_dropdown)
        
        # Try to select by partial text match
        options = select.options
        for option in options:
            if institution_name.lower() in option.text.lower():
                select.select_by_visible_text(option.text)
                return True
        return False
    
    def continue_to_institution(self):
        """Click continue button to proceed to institution login"""
        continue_button = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        continue_button.click()
        
        # Wait for redirect
        self.wait.until(lambda driver: "cilogon.org" not in driver.current_url)
        return True
    
    def get_available_institutions(self):
        """Get list of available institutions"""
        institution_dropdown = self.wait.until(EC.presence_of_element_located(self.INSTITUTION_DROPDOWN))
        select = Select(institution_dropdown)
        return [option.text for option in select.options[1:]]  # Skip default option


class ConnectionListPage(BasePage):
    """Page object for connection list view"""
    
    # Locators
    CONNECTION_TABLE = (By.XPATH, "//table[contains(@class, 'connection') or contains(@class, 'circuit')]")
    CONNECTION_ROWS = (By.XPATH, "//tr[contains(@class, 'connection') or contains(@class, 'circuit')] | //tbody/tr")
    SEARCH_FIELD = (By.XPATH, "//input[@type='text' and contains(@placeholder, 'search')]")
    
    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
    
    def load_connection_list(self):
        """Load connection list page"""
        self.driver.get(f"{self.base_url}/circuits/nodes/list")
        self.wait_for_page_load()
    
    def get_connections(self):
        """Get list of connection elements"""
        try:
            self.wait.until(EC.presence_of_element_located(self.CONNECTION_TABLE))
            return self.driver.find_elements(*self.CONNECTION_ROWS)
        except TimeoutException:
            return []
    
    def search_connections(self, search_term):
        """Search for specific connections"""
        try:
            search_field = self.wait.until(EC.presence_of_element_located(self.SEARCH_FIELD))
            search_field.clear()
            search_field.send_keys(search_term)
            search_field.send_keys(Keys.ENTER)
            time.sleep(2)
            return True
        except TimeoutException:
            return False
    
    def click_connection(self, connection_index=0):
        """Click on a specific connection to view details"""
        connections = self.get_connections()
        if connections and len(connections) > connection_index:
            connections[connection_index].click()
            return True
        return False