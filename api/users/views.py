import json
from jwt import (
    JWT,
    jwk_from_dict,
)
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse


def get_key():
    with open('key.json', 'r') as fh:
        return jwk_from_dict(json.load(fh))


class TokenHandler:
    def __init__(self):
        self.jwt = JWT()
        self.key = get_key()

    def generate_token(self, user):
        payload = {
            'id': user.id,
            'username': user.username,
            'admin': user.is_staff
        }
        return {'token': self.jwt.encode(payload, self.key, 'RS256')}
    
    def decode_token(self, token):
        return self.jwt.decode(token, self.key, 'RS256')

    def get_user_id_token(self, token):
        payload = self.decode_token(token)
        return payload["id"]


tokenHandler = TokenHandler()


class LoginView(CreateAPIView):
    serializer_class = UserSerializer
    model = User

    def post(self, request):
        values = json.loads(request.body)
        user = authenticate(username=values["username"], password=values["password"])
        if user is not None:
            token = tokenHandler.generate_token(user)
            print(token)
            return JsonResponse(token, status=200)
        else:
            return HttpResponse(status=400)


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    model = User

    def post(self, request):
        values = json.loads(request.body)
        user = User.objects.create_user(values["username"], None, values["password"])
        return HttpResponse(status=204)