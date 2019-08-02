import requests
import json
from urllib.parse import unquote

API_URL = "http://127.0.0.1:8001/"

def decode(value):
    while "+" in value:
        value = value.replace("+"," ")
    return unquote(value)

def bodyToJson(body):
    elements = body.split("&")
    data = dict()
    for element in elements:
        items = element.split("=")
        name = decode(items[0])
        value = decode(items[1])
        if "[]" in name:
            name = name.replace("[]","")
            if name not in data:
                data[name] = list()
            data[name].append(value)
        else:
            data[name] = value
    return data

def jsonToDict(url):
    r = requests.get(url)
    return json.loads(r.content.decode('utf-8'))