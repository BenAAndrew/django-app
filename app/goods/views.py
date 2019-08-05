from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.dataHandler import *
from app.tools import *
import json
import requests

def index(request):
    if "message" in request.session:
        message = request.session["message"]
        request.session["message"] = None
        return render(request, 'viewGoods.html', {"goods": getGoods(), "message": message})
    else:
        return render(request, 'viewGoods.html', {"goods": getGoods()})


def createGood(request):
    if request.method == "GET":
        if "message" in request.session:
            message = request.session["message"]
            request.session["message"] = None
            return render(request, 'createGood.html', {"message": message})
        else:
            return render(request, 'createGood.html')
    elif request.method == "POST":
        r = requests.post(API_URL+"application/good/", json=bodyToJson(request.body.decode('utf-8')))
        if r.status_code == 400:
            request.session["message"] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/goods/create/')
        else:
            request.session['message'] = "Successfully created a good"
            return HttpResponseRedirect('/goods/')


def editGood(request, good_id):
    if request.method == "GET":
        if "message" in request.session:
            message = request.session["message"]
            request.session["message"] = None
            return render(request, 'editGood.html', {"good": getGood(good_id), "message": message})
        else:
            return render(request, 'editGood.html', {"good": getGood(good_id)})
    elif request.method == "POST":
        r = requests.put(API_URL+"application/good/" + str(good_id) + "/", json=bodyToJson(request.body.decode('utf-8')))
        if r.status_code == 400:
            request.session['message'] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/goods/edit/'+str(good_id)+"/")
        else:
            request.session['message'] = "Successfully edited a good"
            return HttpResponseRedirect('/goods/')


def viewGood(request, good_id):
    return render(request, 'viewGood.html', {"good": getGood(good_id)})


def deleteGood(request, good_id):
    r = requests.delete(API_URL+"application/good/" + str(good_id) + "/")
    request.session['message'] = "Successfully deleted a good"
    return HttpResponseRedirect('/goods/')
