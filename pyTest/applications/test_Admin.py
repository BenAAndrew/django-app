from chrome import *
from setup import *
from login import login_admin_user
from test_Application import addTestApplication
import requests

def addSubmittedApplication():
    id = addTestApplication()
    requests.get(api_url + "application/submit/" + str(id) + "/")
    return id

class TestAdmin(Chrome):
    @login_admin_user
    def test_view_submitted_applications(self):
        addSubmittedApplication()
        assert len(self.driver.find_elements_by_id("applications")) != 0
        for name in self.driver.find_elements_by_id("app_name"):
            assert len(name.text) != 0
        for progress in self.driver.find_elements_by_id("progress"):
            assert progress.text == "Progress: Submitted"

    @login_admin_user
    def test_review_application(self):
        id = addSubmittedApplication()
        self.driver.get(url + "admin/")
        self.driver.find_elements_by_id("review")[-1].click()
        assert self.driver.current_url == url + "admin/review/" + str(id) +"/"
        assert len(self.driver.find_element_by_id("name").text) != 0
        assert len(self.driver.find_element_by_id("date").text) != 0
        assert len(self.driver.find_element_by_id("destination").text) != 0
        assert "submitted" in self.driver.find_element_by_id("progress").text.lower()
        assert len(self.driver.find_element_by_id("goods_list").text) != 0

class TestReviewingApplications(Chrome):
    @login_admin_user
    def test_accept_application(self):
        id = addSubmittedApplication()
        self.driver.get(url + "admin/")
        self.driver.find_elements_by_id("review")[-1].click()
        self.driver.find_element_by_id("accept").click()
        assert self.driver.current_url == url + "admin/"
        self.driver.get(url + "applications/view/"+str(id)+"/")
        assert "approved" in self.driver.find_element_by_id("progress").text.lower()

    @login_admin_user
    def test_reject_application(self):
        id = addSubmittedApplication()
        self.driver.get(url + "admin/")
        self.driver.find_elements_by_id("review")[-1].click()
        self.driver.find_element_by_id("reject").click()
        assert self.driver.current_url == url + "admin/"
        self.driver.get(url + "applications/view/" + str(id) + "/")
        assert "declined" in self.driver.find_element_by_id("progress").text.lower()