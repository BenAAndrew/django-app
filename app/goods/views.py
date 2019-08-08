from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.userChecks import check_is_user, isAdmin
from app.tools import *

def getGoods(request):
    return decode_request(requests.get("http://127.0.0.1:8001/goods/", cookies=request.COOKIES))

def getGoodsSelected(ids, request):
    allGoods = getGoods(request)
    for i in range(0, len(allGoods)):
        allGoods[i]["selected"] = allGoods[i]["id"] in ids
    return allGoods

def getGood(id, request):
    return decode_request(requests.get('http://127.0.0.1:8001/goods/'+str(id)+"/", cookies=request.COOKIES))

def getGoodsNames(ids, request):
    goods = list()
    for id in ids:
        goods.append({ "id": int(id), "name" : getGood(int(id), request)["name"]})
    return goods

@check_is_user
def index(request):
    if "message" in request.session:
        return render(request, 'viewGoods.html', {"isAdmin" : isAdmin(request), "goods": getGoods(request), "message": getMessage(request)})
    else:
        return render(request, 'viewGoods.html', {"isAdmin" : isAdmin(request), "goods": getGoods(request)})


@check_is_user
def createGood(request):
    if request.method == "GET":
        if "message" in request.session:
            return render(request, 'createGood.html', {"isAdmin" : isAdmin(request), "error": getMessage(request)})
        else:
            return render(request, 'createGood.html', {"isAdmin" : isAdmin(request)})
    elif request.method == "POST":
        data = bodyToJson(request.body.decode('utf-8'))
        data["token"] = request.session["token"]
        r = requests.post(API_URL+"goods/", json=data, cookies=request.COOKIES)
        if r.status_code == 400:
            request.session["message"] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/goods/create/')
        else:
            request.session['message'] = "Successfully created a good"
            return HttpResponseRedirect('/goods/')


@check_is_user
def editGood(request, good_id):
    if request.method == "GET":
        if "message" in request.session:
            return render(request, 'editGood.html', {"isAdmin" : isAdmin(request), "good": getGood(good_id, request), "error": getMessage(request)})
        else:
            return render(request, 'editGood.html', {"isAdmin" : isAdmin(request), "good": getGood(good_id, request)})
    elif request.method == "POST":
        data = bodyToJson(request.body.decode('utf-8'))
        data["token"] = request.session["token"]
        r = requests.put(API_URL+"goods/" + str(good_id) + "/", json=data, cookies=request.COOKIES)
        if r.status_code == 400:
            request.session['message'] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/goods/edit/'+str(good_id)+"/")
        else:
            request.session['message'] = "Successfully edited a good"
            return HttpResponseRedirect('/goods/')


@check_is_user
def viewGood(request, good_id):
    return render(request, 'viewGood.html', {"isAdmin" : isAdmin(request), "good": getGood(good_id, request)})


@check_is_user
def deleteGood(request, good_id):
    r = requests.delete(API_URL+"goods/" + str(good_id) + "/", cookies=request.COOKIES)
    request.session['message'] = "Successfully deleted a good"
    return HttpResponseRedirect('/goods/')
