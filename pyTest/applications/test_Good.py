from chrome import *
from setup import *

class TestGood(Chrome):
    def test_add_good(self):
        for testGood in testGoods:
            self.driver.get(url+ id_to_link["createGood"])
            self.driver.find_element_by_name("name").send_keys(testGood)
            self.driver.find_element_by_id("submit").click()
            self.driver.get(url + id_to_link["viewGood"])
            goodNames = self.driver.find_elements_by_id("good_name")
            assert testGood in [name.text for name in goodNames]

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

    def test_view_good(self):
        self.driver.get(url + id_to_link["viewGood"])
        goodName = self.driver.find_element_by_id("good_name").text
        self.driver.find_element_by_id("view").click()
        assert self.driver.find_element_by_id("good_name").text == goodName

    def test_delete_good(self):
        for i in range(0, len(testGoods)):
            self.driver.get(url + id_to_link["viewGood"])
            totalGoods = len(self.driver.find_elements_by_id("good_name"))
            self.driver.find_element_by_id("edit").click()
            self.driver.find_element_by_id("delete").click()
            self.driver.get(url + id_to_link["viewGood"])
            assert len(self.driver.find_elements_by_id("good_name")) == totalGoods - 1