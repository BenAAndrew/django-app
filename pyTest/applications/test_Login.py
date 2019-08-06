from chrome import *
from setup import *
from login import loginStandardUser

class TestLogin(Chrome):
    def test_redirect(self):
        self.driver.get(url+"applications/")
        assert "You must login first" in self.driver.find_element_by_id("error").text
        assert self.driver.current_url  == url+"login/"

    def test_invalid_login(self):
        self.driver.get(url + "login/")
        self.driver.find_element_by_name("username").send_keys("abc")
        self.driver.find_element_by_name("password").send_keys("123")
        self.driver.find_element_by_id("submit").click()
        assert "User not found" in self.driver.find_element_by_id("error").text
        assert self.driver.current_url == url + "login/"

    def test_valid_login(self):
        loginStandardUser(self)
        assert self.driver.current_url == url + "applications/"