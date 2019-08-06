import json
from jwt import (
    JWT,
    jwk_from_dict,
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse

def getKey():
    with open('key.json', 'r') as fh:
        return jwk_from_dict(json.load(fh))

def login(request):
    values = json.loads(request.body)
    user = authenticate(username=values["username"], password=values["password"])
    if user is not None:
        payload = {
            'username': user.username,
            'admin': user.is_staff
        }
        jwt = JWT()
        token = {'token': jwt.encode(payload, getKey(), 'RS256')}
        print(token)
        return JsonResponse(token, status=200)
    else:
        return HttpResponse(status=400)

def create(request):
    values = json.loads(request.body)
    user = User.objects.create_user(values["username"], None, values["password"])
    return HttpResponse(status=204)