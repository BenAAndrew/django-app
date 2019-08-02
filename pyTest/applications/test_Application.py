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
testGoods = ["testGood","testGoodTwo"]
testApp = {"name" : "testApp", "destination" : "testLocation"}


class TestNavbar(Chrome):
    def test_each_link(self):
        self.driver.get(url+"application/")
        for id in id_to_link:
            self.driver.find_element_by_id(id).click()
            assert self.driver.current_url == url+id_to_link[id]


class TestAddingData(Chrome):
    def test_add_good(self):
        for testGood in testGoods:
            self.driver.get(url+ id_to_link["createGood"])
            self.driver.find_element_by_name("name").send_keys(testGood)
            self.driver.find_element_by_id("submit").click()
            self.driver.get(url + id_to_link["viewGood"])
            goodNames = self.driver.find_elements_by_id("good_name")
            assert testGood in [name.text for name in goodNames]

    def test_add_application(self):
        self.driver.get(url + id_to_link["createApplication"])
        self.driver.find_element_by_name("name").send_keys(testApp["name"])
        self.driver.find_element_by_name("destination").send_keys(testApp["destination"])
        goods = self.driver.find_elements_by_name("goods[]")
        goods[0].click()
        self.driver.find_element_by_id("submit").click()
        appNames = self.driver.find_elements_by_id("app_name")
        assert testApp["name"] in [name.text for name in appNames]


class TestEditingData(Chrome):
    def test_edit_application(self):
        value = "AWholeNewValue"
        self.driver.get(url+id_to_link["home"])
        self.driver.find_elements_by_id("edit")[-1].click()
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys(value)
        self.driver.find_elements_by_name("goods[]")[1].click()
        self.driver.find_element_by_id("edit").click()
        newCard = self.driver.find_elements_by_id("app_name")[-1].text
        assert value == newCard

    def test_edit_good(self):
        value = "goodTest"
        self.driver.get(url+id_to_link['viewGood'])
        self.driver.find_elements_by_id("edit")[-1].click()
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys(value)
        self.driver.find_element_by_id("edit").click()
        self.driver.get(url+id_to_link['viewGood'])
        newCard = self.driver.find_elements_by_id("good_name")[-1].text
        assert value == newCard


class TestViewingData(Chrome):
    def test_view_good(self):
        self.driver.get(url + id_to_link["viewGood"])
        goodName = self.driver.find_element_by_id("good_name").text
        self.driver.find_element_by_id("view").click()
        assert self.driver.find_element_by_id("good_name").text == goodName

    def test_view_application(self):
        self.driver.get(url + id_to_link["home"])
        appName = self.driver.find_element_by_id("app_name").text
        self.driver.find_element_by_id("view").click()
        assert self.driver.find_element_by_id("name").text == appName
        assert self.driver.find_element_by_id("goods").text == "Goods;"
        assert self.driver.find_element_by_id("goods_list")
        assert self.driver.find_elements_by_id("date")
        assert self.driver.find_elements_by_id("destination")


class TestDeletingData(Chrome):
    def test_delete_good(self):
        self.driver.get(url + id_to_link["viewGood"])
        totalGoods = len(self.driver.find_elements_by_id("good_name"))
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete").click()
        self.driver.get(url + id_to_link["viewGood"])
        assert len(self.driver.find_elements_by_id("good_name")) == totalGoods - 1

    def test_delete_application(self):
        self.driver.get(url + id_to_link["home"])
        totalApplications = len(self.driver.find_elements_by_id("app_name"))
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete").click()
        assert len(self.driver.find_elements_by_id("app_name")) == totalApplications - 1