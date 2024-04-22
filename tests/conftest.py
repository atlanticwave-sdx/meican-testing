import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def chrome_driver_init(request):
    web_driver = webdriver.Chrome()
    request.cls.driver = web_driver
    yield
    web_driver.quit()
