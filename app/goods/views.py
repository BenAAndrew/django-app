from django.shortcuts import render
from .dataHandler import *


def index(request):
    return render(request, 'viewGoods.html', { "goods" : getGoods() })


def createGood(request):
    if request.method == "GET":
        return render(request, 'createGood.html')
    elif request.method == "POST":
        r = requests.post(API_URL+"application/good/", json=bodyToJson(request.body.decode('utf-8')))
        if r.status_code == 400:
            errorResponse = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return render(request, 'createGood.html', {"message": errorResponse})
        else:
            return render(request, 'viewGoods.html',
                          { "goods" : getGoods(), "message" : "Successfully created a good" })


def editGood(request, good_id):
    if request.method == "GET":
        return render(request, 'editGood.html', { "good": getGood(good_id) })
    elif request.method == "POST":
        r = requests.put(API_URL+"application/good/" + str(good_id) + "/", json=bodyToJson(request.body.decode('utf-8')))
        if r.status_code == 400:
            errorResponse = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return render(request, 'createapplication/editGood.html',
                          { "good": getGood(good_id), "message": errorResponse})
        else:
            return render(request, 'createapplication/viewGoods.html',
                          { "goods" : getGoods(), "message" : "Successfully edited a good" })


def viewGood(request, good_id):
    return render(request, 'viewGood.html', { "good": getGood(good_id) })


def deleteGood(request, good_id):
    r = requests.delete(API_URL+"application/good/" + str(good_id) + "/")
    return render(request, 'viewGoods.html',
                  { "goods" : getGoods(), "message" : "Successfully deleted a good" })