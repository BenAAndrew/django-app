import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import json

from .serializers import ApplicationSerializer
from .models import Application

def getApplications():
    r = requests.get('http://127.0.0.1:8001/application/')
    return json.loads(r.content.decode('utf-8'))

def index(request):
    return render(request, 'createapplication/index.html', { "applications" : getApplications() })

def detail(request, application_id):
    return HttpResponse("You're looking at question %s." % application_id)

@csrf_exempt
def create(request):
    if request.method == "GET":
        return render(request, 'createapplication/create.html')
    elif request.method == "POST":
        r = requests.post('http://127.0.0.1:8001/application/', data=request.body)
        return render(request, 'createapplication/applicationRedirect.html')