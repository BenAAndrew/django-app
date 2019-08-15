import json
from jwt import (
    JWT,
    jwk_from_dict,
)
from django.http import HttpResponseRedirect


def get_key():
    with open('key.json', 'r') as fh:
        return jwk_from_dict(json.load(fh))


jwt = JWT()
key = get_key()


def decode_token(request):
    try:
        encoded = request.COOKIES['token']
        return jwt.decode(encoded, key, 'RS256')
    except:
        return None


def redirect_to_login(request):
    request.session['error'] = "You must login first"
    return HttpResponseRedirect('/login/')


def redirect_to_home(request):
    request.session['error'] = "You do not have rights to access that page"
    return HttpResponseRedirect('/applications/')


def is_admin(request):
    token = decode_token(request)
    return token is not None and token["admin"]


def check_is_admin(input_func):
    def check(*args, **kwargs):
        if is_admin(*args):
            return input_func(*args, **kwargs)
        else:
            return redirect_to_home(*args)
    return check


def check_is_user(input_func):
    def check(*args, **kwargs):
        if decode_token(*args) is not None:
            return input_func(*args, **kwargs)
        else:
            return redirect_to_login(*args)
    return check
