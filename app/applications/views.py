from django.shortcuts import render
from app.userChecks import check_is_user, isAdmin
from django.http import HttpResponseRedirect
from goods.views import getGoods, getGoodsNames, getGoodsSelected
from app.tools import *

progress = ['draft', 'submitted', 'processing', 'approved']

def progressToProgressPercent(application):
    state = application["progress"]
    if state == 'declined':
        return 5
    else:
        return (progress.index(state)+1) * 25

def getApplications(request):
    applications = decode_request(requests.get("http://127.0.0.1:8001/applications/", cookies=request.COOKIES))
    for i in range(0, len(applications)):
        applications[i]["progress_percent"] = progressToProgressPercent(applications[i])
        applications[i]["progress"] = applications[i]["progress"].capitalize()
    return applications

def getApplication(id, request):
    application = decode_request(requests.get('http://127.0.0.1:8001/applications/'+str(id)+"/", cookies=request.COOKIES))
    application["goods"] = getGoodsNames(application["goods"], request)
    application["goods"] = getGoodsSelected([good["id"] for good in application["goods"]], request)
    return application

@check_is_user
def index(request):
    if "message" in request.session:
        return render(request, 'index.html', {"isAdmin" : isAdmin(request), "applications": getApplications(request), "message" : getMessage(request)})
    else:
        return render(request, 'index.html', {"isAdmin" : isAdmin(request), "applications": getApplications(request)})

@check_is_user
def createApplication(request):
    if request.method == "GET":
        if "message" in request.session:
            return render(request, 'createApplication.html', {"isAdmin" : isAdmin(request), "goods" : getGoods(request), "error": getMessage(request)})
        else:
            return render(request, 'createApplication.html', {"isAdmin" : isAdmin(request), "goods": getGoods(request)})
    elif request.method == "POST":
        data = bodyToJson(request.body.decode('utf-8'))
        data["token"] = request.session["token"]
        r = requests.post(API_URL+"applications/", json=data, cookies=request.COOKIES)
        if r.status_code == 400:
            request.session['message'] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/applications/create/')
        else:
            request.session['message'] = "Successfully created an application"
            return HttpResponseRedirect('/applications/')

@check_is_user
def editApplication(request, application_id):
    if request.method == "GET":
        if "message" in request.session:
            return render(request, 'editApplication.html', {"isAdmin" : isAdmin(request), "application" : getApplication(application_id, request), "error": getMessage(request)})
        else:
            return render(request, 'editApplication.html', {"isAdmin" : isAdmin(request), "application": getApplication(application_id) })
    elif request.method == "POST":
        data = bodyToJson(request.body.decode('utf-8'))
        data["token"] = request.session["token"]
        r = requests.put(API_URL+"applications/"+str(application_id)+"/", json=data, cookies=request.COOKIES)
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
    r = requests.delete(API_URL+"applications/" + str(application_id) + "/", cookies=request.COOKIES)
    request.session['message'] = "Successfully deleted an application"
    return HttpResponseRedirect('/applications/')

@check_is_user
def submitApplication(request, application_id):
    r = requests.get(API_URL + "applications/progress/submitted/" + str(application_id) + "/", cookies=request.COOKIES)
    if r.status_code == 400:
        request.session['message'] = "Error occurred submitting an application"
    else:
        request.session['message'] = "Successfully submitted an application"
    return HttpResponseRedirect('/applications/')
