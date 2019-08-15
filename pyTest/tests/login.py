import json
from setup import *


def get_credentials(user):
    with open('testLogin.json', 'r') as tl:
        credentials = json.load(tl)
    return {"username" : credentials[user]["username"], "password" : credentials[user]["password"]}


def login_form(driver, credentials):
    driver.get(url + "login/")
    driver.find_element_by_name("username").send_keys(credentials["username"])
    driver.find_element_by_name("password").send_keys(credentials["password"])
    driver.find_element_by_id("submit").click()


def logout(self):
    self.driver.get(url + "login/logout")


def loginStandardUser(self):
    login_form(self.driver, get_credentials("user"))


def loginAdminUser(self):
    login_form(self.driver, get_credentials("admin"))


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


def ensure_logged_out(input_func):
    def logged_out(*args, **kwargs):
        logout(*args)
        return input_func(*args, **kwargs)
    return logged_out
