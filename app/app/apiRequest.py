import requests
import json

API_URL = "http://127.0.0.1:8001/"

endpoints = {
                "applications": "applications/",
                "submit": "applications/progress/submitted/",
                "goods": "goods/",
                "admin": "admin/",
                "admin_goods": "admin/goods/",
                "approve": "applications/progress/approved/",
                "decline": "applications/progress/declined/",
                "users": "users/",
                "create_account": "users/create/"
            }


def decode_request(data):
    return json.loads(data.decode('utf-8'))


def build_url(endpoint_name, url_extension):
    url = API_URL + endpoints[endpoint_name]
    if url_extension is not None:
        url += url_extension
    return url


def switch_method(request, url, method, data=None):
    if method == "GET":
        r = requests.get(url, cookies=request.COOKIES)
    elif method == "DELETE":
        r = requests.delete(url, cookies=request.COOKIES)
    elif method == "POST":
        r = requests.post(url, json=data, cookies=request.COOKIES)
    elif method == "PUT":
        r = requests.put(url, json=data, cookies=request.COOKIES)
    else:
        raise AttributeError
    return r


def request_result(r, data_only):
    if data_only:
        return decode_request(r.content)
    else:
        return r


def make_request(request, endpoint_name, method, data=None, url_extension=None, data_only=False):
    url = build_url(endpoint_name, url_extension)
    r = switch_method(request, url, method, data)
    return request_result(r, data_only)


def get_request(request, endpoint_name, url_extension=None, data_only=False):
    return make_request(request, endpoint_name, "GET", url_extension=url_extension, data_only=data_only)


def delete_request(request, endpoint_name, url_extension=None, data_only=False):
    return make_request(request, endpoint_name, "DELETE", url_extension=url_extension, data_only=data_only)


def post_request(request, endpoint_name, data, url_extension=None, data_only=False):
    return make_request(request, endpoint_name, "POST", data=data, url_extension=url_extension, data_only=data_only)


def put_request(request, endpoint_name, data, url_extension=None, data_only=False):
    return make_request(request, endpoint_name, "PUT", data=data, url_extension=url_extension, data_only=data_only)
