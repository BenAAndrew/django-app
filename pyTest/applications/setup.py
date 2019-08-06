import random
import string

url = "http://127.0.0.1:8000/"

api_url = "http://127.0.0.1:8001/"

id_to_link = {"home" : "applications/", "createApplication" : "applications/create/",
              "createGood" : "goods/create/", "viewGood" : "goods/", "logout" : "login/"}

id_to_link_admin = {"admin" : "admin/", "logout" : "login/"}

testApp = {"name" : "testApp", "destination" : "testLocation"}

def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))