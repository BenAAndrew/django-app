from chrome import *
from setup import *
from login import loginStandardUser, loginAdminUser
from test_Application import create_application


def add_submitted_application(self, name, destination, good):
    loginStandardUser(self)
    create_application(self.driver, name, destination, good)
    self.driver.get(url + id_to_link['home'])
    self.driver.find_elements_by_id("submit")[-1].click()
    loginAdminUser(self)


class TestAdmin(Chrome):
    def test_view_submitted_applications(self):
        add_submitted_application(self, randomString(10), randomString(10), randomString(10))
        assert len(self.driver.find_elements_by_id("applications")) != 0
        for name in self.driver.find_elements_by_id("app_name"):
            assert len(name.text) != 0
        for progress in self.driver.find_elements_by_id("progress"):
            assert progress.text == "Progress: submitted"

    def test_review_application(self):
        add_submitted_application(self, randomString(10), randomString(10), randomString(10))
        self.driver.get(url + "admin/")
        self.driver.find_elements_by_id("review")[-1].click()
        assert len(self.driver.find_element_by_id("name").text) != 0
        assert len(self.driver.find_element_by_id("destination").text) != 0
        assert "submitted" in self.driver.find_element_by_id("progress").text.lower()
        assert len(self.driver.find_element_by_id("goods_list").text) != 0


class TestReviewingApplications(Chrome):
    def _review_application(self, button, progress):
        add_submitted_application(self, randomString(10), randomString(10), randomString(10))
        self.driver.get(url + id_to_link_admin["admin"])
        self.driver.find_elements_by_id("review")[-1].click()
        self.driver.find_element_by_id(button).click()
        assert self.driver.current_url == url + id_to_link_admin["admin"]
        loginStandardUser(self)
        self.driver.get(url + id_to_link['home'])
        assert progress in self.driver.find_elements_by_id("progress")[-1].text.lower()

    def test_accept_application(self):
        self._review_application("accept", "approved")

    def test_reject_application(self):
        self._review_application("reject","declined")