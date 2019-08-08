import requests
import json


class RequestsHandler():
    def __init__(self):
        self.r = requests.session()
        self.cookies = dict()

    def set_cookie(self, key, value):
        self.cookies[key] = value

    def get(self):
        req = self.r.get('http://127.0.0.1:8001/applications/', cookies=self.cookies)
        print(json.loads(req.content.decode('utf-8')))
