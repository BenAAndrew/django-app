import pytest
import pytest_html
from selenium import webdriver
from time import sleep

#Fixture for Chrome
from selenium.webdriver.support.select import Select


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
testApp = {"name" : "testApp", "destination" : "testLocation"}


class TestNavbar(Chrome):
    def test_each_link(self):
        self.driver.get(url+"application/")
        for id in id_to_link:
            self.driver.find_element_by_id(id).click()
            assert self.driver.current_url == url+id_to_link[id]


class TestAddingData(Chrome):
    def test_add_good(self):
        self.driver.get(url+ id_to_link["createGood"])
        self.driver.find_element_by_name("name").send_keys(testGood)
        self.driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        self.driver.switch_to.alert.accept()
        self.driver.get(url + id_to_link["viewGood"])
        goodNames = self.driver.find_elements_by_xpath("//div//h1")
        assert testGood in [name.get_attribute('innerHTML') for name in goodNames]

    def test_add_application(self):
        self.driver.get(url + id_to_link["createApplication"])
        self.driver.find_element_by_name("name").send_keys(testApp["name"])
        self.driver.find_element_by_name("destination").send_keys(testApp["destination"])
        select = Select(self.driver.find_element_by_name("goods"))
        select.select_by_visible_text(testGood)
        self.driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        self.driver.switch_to.alert.accept()
        appNames = self.driver.find_elements_by_xpath("//div//h1")
        assert testApp["name"] in [name.get_attribute('innerHTML') for name in appNames]


class TestDeletingData(Chrome):
    def test_delete_good(self):
        self.driver.get(url + id_to_link["viewGood"])
        totalGoods = len(self.driver.find_elements_by_xpath("//div//h1"))
        self.driver.find_element_by_xpath("//button[text()=\"Edit\"]").click()
        self.driver.find_element_by_xpath("//input[@value=\"Delete\"]").click()
        self.driver.switch_to.alert.accept()
        self.driver.get(url + id_to_link["viewGood"])
        assert len(self.driver.find_elements_by_xpath("//div//h1")) == totalGoods - 1

    def test_delete_application(self):
        self.driver.get(url + id_to_link["home"])
        totalApplications = len(self.driver.find_elements_by_xpath("//div//h1"))
        self.driver.find_element_by_xpath("//button[text()=\"Edit\"]").click()
        self.driver.find_element_by_xpath("//input[@value=\"Delete\"]").click()
        self.driver.switch_to.alert.accept()
        assert len(self.driver.find_elements_by_xpath("//div//h1")) == totalApplications - 1


class TestEditingData(Chrome):
    def test_edit_application(self):
        value = "endToEnd"
        self.driver.get(url+id_to_link["home"])
        self.driver.find_element_by_xpath("(//button[@type='button' and text()='Edit'])[1]").click()
        self.driver.find_element_by_xpath("//form//input[@name='name']").clear()
        self.driver.find_element_by_xpath("//form//input[@name='name']").send_keys(value)
        self.driver.find_element_by_xpath("//form//select[@name='goods']//option[1]").click()
        self.driver.find_element_by_xpath("(//input[@type='submit'])[1]").click()
        self.driver.switch_to.alert.accept()
        newCard = self.driver.find_element_by_xpath("(//div[@class='card-body'])//h1").get_attribute('innerHTML')
        assert value == newCard
