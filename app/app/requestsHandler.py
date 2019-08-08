import requests
import json


class RequestsHandler:
    def __init__(self):
        self.r = requests.session()

    def get(self, url, cookies):
        requests.session().cookies["abc"] = "123"
        req = self.r.get(url, cookies=cookies)
        return json.loads(req.content.decode('utf-8'))

    def post(self, url, data, cookies):
        req = self.r.get(url, data=data, cookies=cookies)
        return json.loads(req.content.decode('utf-8'))