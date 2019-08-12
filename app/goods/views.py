from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.userChecks import check_is_user, isAdmin
from app.tools import *
from app.apiRequest import get_request, post_request, put_request, delete_request

def getGoods(request):
    return get_request(request, "goods", data_only=True)

def getGoodsSelected(ids, request):
    allGoods = getGoods(request)
    for i in range(0, len(allGoods)):
        allGoods[i]["selected"] = allGoods[i]["id"] in ids
    return allGoods

def getGood(id, request):
    return get_request(request, "goods", data_only=True, url_extension=str(id)+"/")

def getGoodsNames(ids, request):
    goods = list()
    for id in ids:
        goods.append({ "id": int(id), "name" : getGood(int(id), request)["name"]})
    return goods


@check_is_user
def index(request):
    data = {"isAdmin" : isAdmin(request), "goods": getGoods(request)}
    if "message" in request.session:
        data["message"] = get_message(request)
    return render(request, 'viewGoods.html', data)


@check_is_user
def createGood(request):
    if request.method == "GET":
        data = {"isAdmin" : isAdmin(request)}
        if "message" in request.session:
            data["error"] = get_message(request)
        return render(request, 'createGood.html', data)
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        r = post_request(request, "goods", data)
        if r.status_code == 400:
            request.session["message"] = handle_error_response(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/goods/create/')
        else:
            request.session['message'] = "Successfully created a good"
            return HttpResponseRedirect('/goods/')


@check_is_user
def editGood(request, good_id):
    if request.method == "GET":
        data = {"isAdmin": isAdmin(request), "good": getGood(good_id, request)}
        if "message" in request.session:
            data["error"] = get_message(request)
        return render(request, 'editGood.html', data)
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        r = put_request(request, "goods", data, url_extension=str(good_id)+"/")
        if r.status_code == 400:
            request.session['message'] = handle_error_response(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/goods/edit/'+str(good_id)+"/")
        else:
            request.session['message'] = "Successfully edited a good"
            return HttpResponseRedirect('/goods/')


@check_is_user
def viewGood(request, good_id):
    return render(request, 'viewGood.html', {"isAdmin" : isAdmin(request), "good": getGood(good_id, request)})


@check_is_user
def deleteGood(request, good_id):
    r = delete_request(request, "goods", url_extension=str(good_id)+"/")
    request.session['message'] = "Successfully deleted a good"
    return HttpResponseRedirect('/goods/')
