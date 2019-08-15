from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.userChecks import check_is_user, is_admin
from app.tools import form_body_to_json, handle_error_response, get_message_or_error
from app.apiRequest import get_request, post_request, put_request, delete_request
import json


def get_goods(request):
    return get_request(request, "goods", data_only=True)


def get_selected_goods(ids, request):
    allGoods = get_goods(request)
    for i in range(0, len(allGoods)):
        allGoods[i]["selected"] = allGoods[i]["id"] in ids
    return allGoods


def get_good(id, request):
    return get_request(request, "goods", data_only=True, url_extension=str(id)+"/")


def get_goods_names(ids, request):
    goods = list()
    for id in ids:
        goods.append({"id": int(id), "name": get_good(int(id), request)["name"]})
    return goods


@check_is_user
def index(request):
    data = {"isAdmin" : is_admin(request), "goods": get_goods(request)}
    msg = get_message_or_error(request)
    if msg:
        data.update(msg)
    return render(request, 'viewGoods.html', data)


@check_is_user
def create_good(request):
    if request.method == "GET":
        data = {"isAdmin": is_admin(request)}
        msg = get_message_or_error(request)
        if msg:
            data.update(msg)
        return render(request, 'createGood.html', data)
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        r = post_request(request, "goods", data)
        if r.status_code == 400:
            request.session["error"] = handle_error_response(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/goods/create/')
        else:
            request.session['message'] = "Successfully created a good"
            return HttpResponseRedirect('/goods/')


@check_is_user
def edit_good(request, good_id):
    if request.method == "GET":
        data = {"isAdmin": is_admin(request), "good": get_good(good_id, request)}
        msg = get_message_or_error(request)
        if msg:
            data.update(msg)
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
def view_good(request, good_id):
    return render(request, 'viewGood.html', {"isAdmin": is_admin(request), "good": get_good(good_id, request)})


@check_is_user
def delete_good(request, good_id):
    delete_request(request, "goods", url_extension=str(good_id)+"/")
    request.session['message'] = "Successfully deleted a good"
    return HttpResponseRedirect('/goods/')
