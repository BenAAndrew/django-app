import requests
from django.http import HttpResponse
from django.shortcuts import render
import json
from urllib.parse import unquote

def decode(value):
    while "+" in value:
        value = value.replace("+"," ")
    return unquote(value)

def bodyToJson(body):
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

def getApplications():
    r = requests.get('http://127.0.0.1:8001/application/')
    return json.loads(r.content.decode('utf-8'))

def getGoods():
    r = requests.get('http://127.0.0.1:8001/application/good/')
    return json.loads(r.content.decode('utf-8'))

def getGoodsSelected(ids):
    allGoods = getGoods()
    for i in range(0, len(allGoods)):
        allGoods[i]["selected"] = allGoods[i]["id"] in ids
    return allGoods

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
        application["goods"] = getGoodsSelected(application["goods"])
        return render(request, 'createapplication/editApplication.html', { "application" : application })
    elif request.method == "POST":
        print(bodyToJson(request.body.decode('utf-8')))
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
