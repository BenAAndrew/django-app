from chrome import *
from setup import *
from login import login_standard_user, login_admin_user, ensure_logged_out

class TestFailedLogins(Chrome):
    def test_invalid_login(self):
        self.driver.get(url + "login/")
        self.driver.find_element_by_name("username").send_keys("abc")
        self.driver.find_element_by_name("password").send_keys("123")
        self.driver.find_element_by_id("submit").click()
        assert "User not found" in self.driver.find_element_by_id("error").text
        assert self.driver.current_url == url + "login/"

class TestSuccessfulLogins(Chrome):
    @login_standard_user
    def test_valid_login(self):
        assert self.driver.current_url == url + "applications/"

    @login_admin_user
    def test_valid_admin_login(self):
        assert self.driver.current_url == url + "admin/"

class TestAccessRights(Chrome):
    @ensure_logged_out
    def test_user_must_be_logged_in(self):
        self.driver.get(url+"applications/")
        assert "You must login first" in self.driver.find_element_by_id("error").text
        assert self.driver.current_url  == url+"login/"

    @login_standard_user
    def test_user_cannot_access_admin_features(self):
        self.driver.get(url+"admin/")
        assert "You do not have rights to access that page" in self.driver.find_element_by_id("error").text
        assert self.driver.current_url == url + "applications/"