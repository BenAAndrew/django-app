import json
from setup import *


def get_credentials(isAdmin):
    with open('testLogin.json', 'r') as tl:
        credentials = json.load(tl)
    return {"username" : credentials["user"]["username"], "password" : credentials["user"]["password"]}


def login_form(self, credentials):
    self.driver.get(url + "login/")
    self.driver.find_element_by_name("username").send_keys(credentials["username"])
    self.driver.find_element_by_name("password").send_keys(credentials["password"])
    self.driver.find_element_by_id("submit").click()


def loginStandardUser(self):
    login_form(self, get_credentials(False))


def loginAdminUser(self):
    login_form(self, get_credentials(True))


def login_standard_user(input_func):
    def login(*args, **kwargs):
        loginStandardUser(*args)
        return input_func(*args, **kwargs)
    return login


def login_admin_user(input_func):
    def login(*args, **kwargs):
        loginAdminUser(*args)
        return input_func(*args, **kwargs)
    return login