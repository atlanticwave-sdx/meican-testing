import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def chrome_driver_init(request):

    # Set to True for headless mode, False for normal mode
    headless_mode = True

    options = webdriver.ChromeOptions()
    if headless_mode:
        options.add_argument("--headless")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")

    web_driver = webdriver.Chrome(options=options)
    request.cls.driver = web_driver
    yield
    web_driver.quit()
