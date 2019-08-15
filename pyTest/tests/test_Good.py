from chrome import *
from setup import *
from login import login_standard_user


def create_good(driver, name):
    driver.get(url + id_to_link["createGood"])
    driver.find_element_by_name("name").send_keys(name)
    driver.find_element_by_id("submit").click()


class TestGood(Chrome):
    @login_standard_user
    def test_add_good(self):
        testGood = randomString(10)
        create_good(self.driver, testGood)
        self.driver.get(url + id_to_link["viewGood"])
        goodNames = self.driver.find_elements_by_id("good_name")
        assert testGood in [name.text for name in goodNames]

    @login_standard_user
    def test_edit_good(self):
        create_good(self.driver, randomString(10))
        newVal = "abc"
        self.driver.get(url+id_to_link['viewGood'])
        self.driver.find_elements_by_id("edit")[-1].click()
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys(newVal)
        self.driver.find_element_by_id("edit").click()
        self.driver.get(url+id_to_link['viewGood'])
        newCard = self.driver.find_elements_by_id("good_name")[-1].text
        assert newVal == newCard

    @login_standard_user
    def test_view_good(self):
        create_good(self.driver, randomString(10))
        self.driver.get(url + id_to_link["viewGood"])
        goodName = self.driver.find_element_by_id("good_name").text
        self.driver.find_element_by_id("view").click()
        assert self.driver.find_element_by_id("good_name").text == goodName

    @login_standard_user
    def test_delete_good(self):
        create_good(self.driver, randomString(10))
        self.driver.get(url + id_to_link["viewGood"])
        totalGoods = len(self.driver.find_elements_by_id("good_name"))
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete").click()
        self.driver.get(url + id_to_link["viewGood"])
        assert len(self.driver.find_elements_by_id("good_name")) == totalGoods - 1