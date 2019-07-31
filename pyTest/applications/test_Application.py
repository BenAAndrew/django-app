import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chromedriver = webdriver.chrome()
    request.cls.driver = chromedriver
    yield
    chromedriver.close()

@pytest.mark.usefixtures("chrome_driver_init")
class basic_chrome_test:
    pass
class test_url_chrome(basic_chrome_test):
    def test_open_url(self):
        self.driver.get("https://www.amazon.co.uk/")
        print(self.driver.title)

        sleep(5)

