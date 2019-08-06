from chrome import *
from setup import *

class TestApplication(Chrome):
    def test_add_application(self):
        self.driver.get(url + id_to_link["createApplication"])
        self.driver.find_element_by_name("name").send_keys(testApp["name"])
        self.driver.find_element_by_name("destination").send_keys(testApp["destination"])
        goods = self.driver.find_elements_by_name("goods[]")
        goods[0].click()
        self.driver.find_element_by_id("submit").click()
        appNames = self.driver.find_elements_by_id("app_name")
        assert testApp["name"] in [name.text for name in appNames]

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

    def test_view_application(self):
        self.driver.get(url + id_to_link["home"])
        appName = self.driver.find_element_by_id("app_name").text
        self.driver.find_element_by_id("view").click()
        assert self.driver.find_element_by_id("name").text == appName
        assert self.driver.find_element_by_id("goods").text == "Goods;"
        assert self.driver.find_element_by_id("goods_list")
        assert self.driver.find_elements_by_id("date")
        assert self.driver.find_elements_by_id("destination")

    def test_delete_application(self):
        self.driver.get(url + id_to_link["home"])
        totalApplications = len(self.driver.find_elements_by_id("app_name"))
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete").click()
        assert len(self.driver.find_elements_by_id("app_name")) == totalApplications - 1