from django.shortcuts import render
from app.userChecks import check_is_admin, isAdmin
from django.http import HttpResponseRedirect
from applications.views import progressToProgressPercent
from app.tools import *


def getApplications(request):
    applications = decode_request(requests.get("http://127.0.0.1:8001/admin/", cookies=request.COOKIES))
    for i in range(0, len(applications)):
        applications[i]["progress_percent"] = progressToProgressPercent(applications[i])
        applications[i]["progress"] = applications[i]["progress"].capitalize()
    return applications

def getGoods(request):
    return decode_request(requests.get("http://127.0.0.1:8001/admin/goods/", cookies=request.COOKIES))

def getGood(id, request):
    return decode_request(requests.get('http://127.0.0.1:8001/admin/goods/'+str(id)+"/", cookies=request.COOKIES))

def getGoodsNames(ids, request):
    goods = list()
    for id in ids:
        goods.append({ "id": int(id), "name" : getGood(int(id), request)["name"]})
    return goods

def getGoodsSelected(ids, request):
    allGoods = getGoods(request)
    for i in range(0, len(allGoods)):
        allGoods[i]["selected"] = allGoods[i]["id"] in ids
    return allGoods

def getApplication(id, request):
    application = decode_request(requests.get('http://127.0.0.1:8001/admin/'+str(id)+"/", cookies=request.COOKIES))
    application["goods"] = getGoodsNames(application["goods"], request)
    application["goods"] = getGoodsSelected([good["id"] for good in application["goods"]], request)
    return application

@check_is_admin
def index(request):
    return render(request, 'admin.html', {"isAdmin" : isAdmin(request), "applications": getApplications(request)})


@check_is_admin
def review(request, application_id):
    return render(request, 'reviewApplication.html', {"isAdmin" : isAdmin(request), "application": getApplication(application_id, request)})


@check_is_admin
def accept(request, application_id):
    r = requests.get(API_URL + "applications/progress/approved/" + str(application_id) + "/")
    if r.status_code == 400:
        request.session['message'] = "Error occurred when accepting application"
    else:
        request.session['message'] = "Successfully accepted an application"
    return HttpResponseRedirect('/admin/')


@check_is_admin
def reject(request, application_id):
    r = requests.get(API_URL + "applications/progress/declined/" + str(application_id) + "/")
    if r.status_code == 400:
        request.session['message'] = "Error occurred when rejecting application"
    else:
        request.session['message'] = "Successfully rejected an application"
    return HttpResponseRedirect('/admin/')
