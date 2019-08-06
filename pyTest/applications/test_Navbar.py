from chrome import *
from setup import *
from login import login_standard_user

class TestNavbar(Chrome):
    @login_standard_user
    def test_each_link(self):
        for id in id_to_link:
            x = id
            self.driver.find_element_by_id(id).click()
            assert self.driver.current_url == url+id_to_link[id]