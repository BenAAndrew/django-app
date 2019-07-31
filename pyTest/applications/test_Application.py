import pytest
import pytest_html
from selenium import webdriver

#Fixture for Chrome
@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chrome_driver = webdriver.Chrome()
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()

@pytest.mark.usefixtures("chrome_driver_init")
class Chrome:
    pass

class TestClass(Chrome):
    def test_one(self):
        self.driver.get("https://www.amazon.co.uk/")
