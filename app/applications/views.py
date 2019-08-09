from django.shortcuts import render
from app.userChecks import check_is_user, isAdmin
from django.http import HttpResponseRedirect
from goods.views import getGoods, getGoodsNames, getGoodsSelected
from app.tools import *
from app.apiRequest import get_request, post_request, put_request, delete_request

progress = ['draft', 'submitted', 'processing', 'approved']

def progressToProgressPercent(application):
    state = application["progress"]
    if state == 'declined':
        return 5
    else:
        return (progress.index(state)+1) * 25

def getApplications(request):
    applications = get_request(request, "applications", data_only=True)
    for i in range(0, len(applications)):
        applications[i]["progress_percent"] = progressToProgressPercent(applications[i])
        applications[i]["progress"] = applications[i]["progress"].capitalize()
    return applications

def getApplication(id, request):
    application = get_request(request, "applications", url_extension=str(id)+"/", data_only=True)
    application["goods"] = getGoodsNames(application["goods"], request)
    application["goods"] = getGoodsSelected([good["id"] for good in application["goods"]], request)
    return application

@check_is_user
def index(request):
    data = {"isAdmin" : isAdmin(request), "applications": getApplications(request)}
    if "message" in request.session:
        data["message"] = getMessage(request)
    return render(request, 'index.html', data)

@check_is_user
def createApplication(request):
    if request.method == "GET":
        data = {"isAdmin" : isAdmin(request), "goods" : getGoods(request)}
        if "message" in request.session:
            data["error"] = getMessage(request)
        return render(request, 'createApplication.html', data)
    elif request.method == "POST":
        data = bodyToJson(request.body.decode('utf-8'))
        r = post_request(request, "applications", data)
        if r.status_code == 400:
            request.session['message'] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/applications/create/')
        else:
            request.session['message'] = "Successfully created an application"
            return HttpResponseRedirect('/applications/')

@check_is_user
def editApplication(request, application_id):
    if request.method == "GET":
        data = {"isAdmin" : isAdmin(request), "application": getApplication(application_id, request)}
        if "message" in request.session:
            data["error"] = getMessage(request)
        return render(request, 'editApplication.html', data)
    elif request.method == "POST":
        data = bodyToJson(request.body.decode('utf-8'))
        r = put_request(request, "applications", data, url_extension=str(application_id)+"/")
        if r.status_code == 400:
            request.session['message'] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/applications/edit/'+str(application_id)+"/")
        else:
            request.session['message'] = "Successfully edited an application"
            return HttpResponseRedirect('/applications/')

@check_is_user
def viewApplication(request, application_id):
    return render(request, 'viewApplication.html', {"isAdmin" : isAdmin(request), "application" : getApplication(application_id, request)})

@check_is_user
def deleteApplication(request, application_id):
    r = delete_request(request, "applications", url_extension=str(application_id)+"/")
    request.session['message'] = "Successfully deleted an application"
    return HttpResponseRedirect('/applications/')

@check_is_user
def submitApplication(request, application_id):
    r = get_request(request, "submit", url_extension=str(application_id)+"/")
    if r.status_code == 400:
        request.session['message'] = "Error occurred submitting an application"
    else:
        request.session['message'] = "Successfully submitted an application"
    return HttpResponseRedirect('/applications/')
