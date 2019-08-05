from django.shortcuts import render
import json
from jwt import (
    JWT,
    jwk_from_dict,
)

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

def check_is_user(request):
    return decodeToken(request) is not None

def check_is_admin(request):
    token = decodeToken(request)
    return token is not None and token["admin"]