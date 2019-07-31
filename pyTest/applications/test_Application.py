import pytest
import pytest_html
from selenium import webdriver
from time import sleep

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

url = "http://127.0.0.1:8000/"
id_to_link = {"home" : "application/", "createApplication" : "application/create/",
              "createGood" : "application/creategood/", "viewGood" : "application/goods/"}
testGood = "testGood"

class TestNavbar(Chrome):
    def test_each_link(self):
        self.driver.get(url+"application/")
        for id in id_to_link:
            self.driver.find_element_by_id(id).click()
            assert self.driver.current_url == url+id_to_link[id]

class TestAddingData(Chrome):
    def test_add_good(self):
        self.driver.get(url+"application/creategood/")
        self.driver.find_element_by_name("name").send_keys(testGood)
        self.driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        self.driver.switch_to.alert.accept()
        self.driver.get(url + "application/goods/")
        goodNames = self.driver.find_elements_by_xpath("//div//h1")
        assert testGood in [name.get_attribute('innerHTML') for name in goodNames]
