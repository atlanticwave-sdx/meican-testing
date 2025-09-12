import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import ssl_handle
from conftest import chrome_driver_init
import urls
import time


class Test_Debug_Cookies(ssl_handle.SSLBaseTest):

    def test_debug_cookie_elements(self):
        """Debug test to identify cookie popup elements on ORCID page"""
        self.handle_ssl_warning(urls.all_urls['USER_LOGIN_URL'])
        
        # Click CILogon button
        cilogon_login_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='wayflogonbutton']"))
        )
        cilogon_login_element.click()
        
        # Wait for CILogon page
        WebDriverWait(self.driver, 15).until(
            lambda driver: "cilogon.org" in driver.current_url
        )
        
        # Select ORCID from dropdown
        from selenium.webdriver.support.ui import Select
        institution_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "idp"))
        )
        select = Select(institution_dropdown)
        
        # Find ORCID option
        for option in select.options:
            if "orcid" in option.text.lower():
                select.select_by_visible_text(option.text)
                break
        
        # Click Log On button
        continue_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='wayflogonbutton']"))
        )
        continue_button.click()
        
        # Wait for ORCID page to load
        WebDriverWait(self.driver, 15).until(
            lambda driver: "orcid.org" in driver.current_url
        )
        
        # Wait for page to fully load
        time.sleep(5)
        
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page title: {self.driver.title}")
        
        # Look for all buttons on the page
        all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(all_buttons)} buttons on page:")
        
        for i, button in enumerate(all_buttons):
            try:
                button_text = button.text
                button_id = button.get_attribute('id')
                button_class = button.get_attribute('class')
                print(f"  Button {i+1}: text='{button_text}', id='{button_id}', class='{button_class}'")
            except:
                pass
        
        # Look for all divs with 'accept' or 'cookie' in id/class
        cookie_elements = self.driver.find_elements(By.XPATH, "//*[contains(@id, 'cookie') or contains(@class, 'cookie') or contains(@id, 'accept') or contains(@class, 'accept')]")
        print(f"Found {len(cookie_elements)} potential cookie elements:")
        
        for i, element in enumerate(cookie_elements):
            try:
                element_tag = element.tag_name
                element_text = element.text
                element_id = element.get_attribute('id')
                element_class = element.get_attribute('class')
                print(f"  Element {i+1}: tag='{element_tag}', text='{element_text[:50]}...', id='{element_id}', class='{element_class}'")
            except:
                pass
        
        # Take a screenshot for debugging
        self.driver.save_screenshot("/tmp/cookie_debug.png")
        print("Screenshot saved to /tmp/cookie_debug.png")


if __name__ == "__main__":
    pytest.main()