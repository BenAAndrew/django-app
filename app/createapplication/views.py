import requests
from django.http import HttpResponse
from django.shortcuts import render
import json

def getApplications():
    r = requests.get('http://127.0.0.1:8001/application/')
    return json.loads(r.content.decode('utf-8'))

def getGoods():
    r = requests.get('http://127.0.0.1:8001/application/good/')
    return json.loads(r.content.decode('utf-8'))

def index(request):
    return render(request, 'createapplication/index.html', { "applications" : getApplications() })

def detail(request, application_id):
    return HttpResponse("You're looking at question %s." % application_id)

def createGood(request):
    if request.method == "GET":
        return render(request, 'createapplication/createGood.html')
    elif request.method == "POST":
        r = requests.post('http://127.0.0.1:8001/application/good/', data=request.body)
        return render(request, 'createapplication/applicationRedirect.html')

def createApplication(request):
    if request.method == "GET":
        return render(request, 'createapplication/createApplication.html', { "goods" : getGoods() })
    elif request.method == "POST":
        r = requests.post('http://127.0.0.1:8001/application/', data=request.body)
        return render(request, 'createapplication/applicationRedirect.html')
