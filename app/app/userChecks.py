from django.shortcuts import render
import json
from jwt import (
    JWT,
    jwk_from_dict,
)
from django.http import HttpResponseRedirect

jwt = JWT()

def getKey():
    with open('key.json', 'r') as fh:
        return jwk_from_dict(json.load(fh))


def decodeToken(request):
    try:
        encoded = request.session["token"]
        return jwt.decode(encoded, getKey(), 'RS256')
    except:
        return None


def redirectToLogin(request):
    request.session['message'] = "You must login first"
    return HttpResponseRedirect('/login/')


def redirectToHome(request):
    request.session['message'] = "You do not have rights to access that page"
    return HttpResponseRedirect('/applications/')


def isAdmin(request):
    token = decodeToken(request)
    return token is not None and token["admin"]


def check_is_admin(input_func):
    def check(*args, **kwargs):
        if isAdmin(*args):
            return input_func(*args, **kwargs)
        else:
            return redirectToHome(*args)
    return check


def check_is_user(input_func):
    def check(*args, **kwargs):
        if decodeToken(*args) is not None:
            return input_func(*args, **kwargs)
        else:
            return redirectToLogin(*args)
    return check
