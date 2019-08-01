import requests
from django.http import HttpResponse
from django.shortcuts import render
import json
import html

def decodeSpaces(value):
    while "+" in value:
        value = value.replace("+"," ")
    return value

def bodyToJson(body):
    elements = body.split("&")
    values = dict()
    for element in elements:
        data = element.split("=")
        data[1] = decodeSpaces(html.unescape(data[1]))
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

def getGoodsNames(ids):
    goods = list()
    for id in ids:
        goods.append({ "id": int(id), "name" : getGood(int(id))["name"]})
    return goods

def index(request):
    return render(request, 'createapplication/index.html', { "applications" : getApplications() })

def detail(request, application_id):
    return HttpResponse("You're looking at question %s." % application_id)

def createGood(request):
    if request.method == "GET":
        return render(request, 'createapplication/createGood.html')
    elif request.method == "POST":
        r = requests.post('http://127.0.0.1:8001/application/good/', json=bodyToJson(request.body.decode('utf-8')))
        return render(request, 'createapplication/viewGoods.html',
                      { "goods" : getGoods(), "message" : "Successfully created a good" })

def editApplication(request, application_id):
    if request.method == "GET":
        application = getApplication(application_id)
        application["goods"] = getGoods()
        return render(request, 'createapplication/editApplication.html', { "application" : application })
    elif request.method == "POST":
        r = requests.put('http://127.0.0.1:8001/application/'+str(application_id)+"/", json=bodyToJson(request.body.decode('utf-8')))
        return render(request, 'createapplication/index.html',
                      { "applications" : getApplications(), "message" : "Successfully edited an application" })

def deleteApplication(request, application_id):
    r = requests.delete('http://127.0.0.1:8001/application/' + str(application_id) + "/")
    return render(request, 'createapplication/index.html',
                  { "applications" : getApplications(), "message" : "Successfully deleted an application" })

def viewApplication(request, application_id):
    application = getApplication(application_id)
    application["goods"] = getGoodsNames(application["goods"])
    return render(request, 'createapplication/viewApplication.html', { "application" : application })

def viewGood(request, good_id):
    return render(request, 'createapplication/viewGood.html', { "good": getGood(good_id) })

def deleteGood(request, good_id):
    r = requests.delete('http://127.0.0.1:8001/application/good/' + str(good_id) + "/")
    return render(request, 'createapplication/viewGoods.html',
                  { "goods" : getGoods(), "message" : "Successfully deleted a good" })

def editGood(request, good_id):
    if request.method == "GET":
        return render(request, 'createapplication/editGood.html', { "good": getGood(good_id) })
    elif request.method == "POST":
        r = requests.put('http://127.0.0.1:8001/application/good/' + str(good_id) + "/", json=bodyToJson(request.body.decode('utf-8')))
        return render(request, 'createapplication/viewGoods.html',
                      { "goods" : getGoods(), "message" : "Successfully edited a good" })

def viewGoods(request):
    return render(request, 'createapplication/viewGoods.html', { "goods" : getGoods() })

def createApplication(request):
    if request.method == "GET":
        return render(request, 'createapplication/createApplication.html', { "goods" : getGoods() })
    elif request.method == "POST":
        print(bodyToJson(request.body.decode('utf-8')))
        r = requests.post('http://127.0.0.1:8001/application/', json=bodyToJson(request.body.decode('utf-8')))
        return render(request, 'createapplication/index.html',
                      { "applications" : getApplications(), "message" : "Successfully created an application" })
