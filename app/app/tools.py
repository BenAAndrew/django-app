import json
from urllib.parse import unquote


def decode(value):
    while "+" in value:
        value = value.replace("+"," ")
    return unquote(value)


def form_body_to_json(body):
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


def decode_request(request):
    return json.loads(request.content.decode('utf-8'))


def handle_error_response(error):
    message = ""
    for key in error:
        message += key + ": " + error[key][0]
    return message


def get_message(request):
    message = request.session["message"]
    del request.session["message"]
    return message


def get_error(request):
    error = request.session["error"]
    del request.session["error"]
    return error
