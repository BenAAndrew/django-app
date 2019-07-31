import requests
from django.http import HttpResponse
from django.shortcuts import render
import json

def bodyToJson(body):
    elements = body.split("&")
    values = dict()
    for element in elements:
        data = element.split("=")
        if data[0] in values:
            if not isinstance(values[data[0]], list):
                copy = values[data[0]]
                values[data[0]] = list()
                values[data[0]].append(copy)
            values[data[0]].append(data[1])
        else:
            values[data[0]] = data[1]
    return values

def getApplications():
    r = requests.get('http://127.0.0.1:8001/application/')
    return json.loads(r.content.decode('utf-8'))

def getGoods():
    r = requests.get('http://127.0.0.1:8001/application/good/')
    return json.loads(r.content.decode('utf-8'))

def getApplication(id):
    r = requests.get('http://127.0.0.1:8001/application/'+str(id)+"/")
    return json.loads(r.content.decode('utf-8'))

def getGood(id):
    print('http://127.0.0.1:8001/application/good/'+str(id)+"/")
    r = requests.get('http://127.0.0.1:8001/application/good/'+str(id)+"/")
    return json.loads(r.content.decode('utf-8'))

def index(request):
    return render(request, 'createapplication/index.html', { "applications" : getApplications() })

def detail(request, application_id):
    return HttpResponse("You're looking at question %s." % application_id)

def createGood(request):
    if request.method == "GET":
        return render(request, 'createapplication/createGood.html')
    elif request.method == "POST":
        r = requests.post('http://127.0.0.1:8001/application/good/', json=bodyToJson(request.body.decode('utf-8')))
        return render(request, 'createapplication/applicationRedirect.html')

def editApplication(request, application_id):
    if request.method == "GET":
        application = getApplication(application_id)
        print(len(application['goods']))
        return render(request, 'createapplication/editApplication.html', { "application" : application })
    if request.method == "POST":
        r = requests.delete('http://127.0.0.1:8001/application/'+str(application_id)+"/")
        return render(request, 'createapplication/applicationRedirect.html')

def editGood(request, good_id):
    if request.method == "GET":
        return render(request, 'createapplication/editGood.html', { "good": getGood(good_id) })
    if request.method == "POST":
        r = requests.delete('http://127.0.0.1:8001/application/good/'+str(good_id)+"/")
        return render(request, 'createapplication/applicationRedirect.html')

def viewGoods(request):
    return render(request, 'createapplication/viewGoods.html', { "goods" : getGoods() })

def createApplication(request):
    if request.method == "GET":
        return render(request, 'createapplication/createApplication.html', { "goods" : getGoods() })
    elif request.method == "POST":
        r = requests.post('http://127.0.0.1:8001/application/', json=bodyToJson(request.body.decode('utf-8')))
        return render(request, 'createapplication/applicationRedirect.html')
