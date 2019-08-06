import json

from chrome import *
from setup import *
from login import login_standard_user
import requests

def addTestApplication():
    r = requests.get(api_url + "goods/")
    test_id = str(json.loads(r.content.decode('utf-8'))[0]["id"])
    r = requests.post(api_url + "application/", json={"name": randomString(10), "destination": "test", "goods": [test_id]})
    return json.loads(r.content.decode('utf-8'))["id"]

class TestApplication(Chrome):
    @login_standard_user
    def test_add_application(self):
        self.driver.get(url + id_to_link["createApplication"])
        self.driver.find_element_by_name("name").send_keys(testApp["name"])
        self.driver.find_element_by_name("destination").send_keys(testApp["destination"])
        goods = self.driver.find_elements_by_name("goods[]")
        goods[0].click()
        self.driver.find_element_by_id("submit").click()
        appNames = self.driver.find_elements_by_id("app_name")
        assert testApp["name"] in [name.text for name in appNames]

    @login_standard_user
    def test_edit_application(self):
        addTestApplication()
        value = "AWholeNewValue"+randomString(10)
        self.driver.get(url+id_to_link["home"])
        self.driver.find_elements_by_id("edit")[-1].click()
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys(value)
        self.driver.find_element_by_id("edit").click()
        self.driver.get(url + id_to_link["home"])
        newCard = self.driver.find_elements_by_id("app_name")[-1].text
        assert value == newCard

    @login_standard_user
    def test_view_application(self):
        self.driver.get(url + id_to_link["home"])
        appName = self.driver.find_element_by_id("app_name").text
        self.driver.find_element_by_id("view").click()
        assert self.driver.find_element_by_id("name").text == appName
        assert self.driver.find_element_by_id("goods").text == "Goods;"
        assert self.driver.find_element_by_id("goods_list")
        assert self.driver.find_elements_by_id("date")
        assert self.driver.find_elements_by_id("destination")

    @login_standard_user
    def test_delete_application(self):
        self.driver.get(url + id_to_link["home"])
        totalApplications = len(self.driver.find_elements_by_id("app_name"))
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete").click()
        assert len(self.driver.find_elements_by_id("app_name")) == totalApplications - 1