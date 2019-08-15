from chrome import *
from setup import *
from login import login_standard_user
from test_Good import create_good


def create_application(driver, name, destination, good):
    create_good(driver, good)
    driver.get(url + id_to_link['createApplication'])
    driver.find_element_by_name("name").send_keys(name)
    driver.find_element_by_name("destination").send_keys(destination)
    driver.find_elements_by_name("goods[]")[0].click()
    driver.find_element_by_id("submit").click()


class TestApplication(Chrome):
    @login_standard_user
    def test_add_application(self):
        create_application(self.driver, testApp["name"], randomString(10), randomString(10))
        self.driver.get(url + id_to_link['home'])
        appNames = self.driver.find_elements_by_id("app_name")
        assert testApp["name"] in [name.text for name in appNames]

    @login_standard_user
    def test_edit_application(self):
        create_application(self.driver, randomString(10), randomString(10), randomString(10))
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
        create_application(self.driver, randomString(10), randomString(10), randomString(10))
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
        create_application(self.driver, randomString(10), randomString(10), randomString(10))
        self.driver.get(url + id_to_link["home"])
        totalApplications = len(self.driver.find_elements_by_id("app_name"))
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete").click()
        assert len(self.driver.find_elements_by_id("app_name")) == totalApplications - 1