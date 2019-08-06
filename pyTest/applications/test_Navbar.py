from chrome import *
from setup import *
from login import login_standard_user, login_admin_user

class TestNavbar(Chrome):
    @login_standard_user
    def test_user_navbar(self):
        for id in id_to_link:
            self.driver.find_element_by_id(id).click()
            assert self.driver.current_url == url+id_to_link[id]

    @login_admin_user
    def test_admin_navbar(self):
        for id in id_to_link_admin:
            self.driver.find_element_by_id(id).click()
            assert self.driver.current_url == url + id_to_link_admin[id]