from django.shortcuts import render
from app.dataHandler import *
from app.userChecks import check_is_user, isAdmin
from django.http import HttpResponseRedirect


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
            return render(request, 'createApplication.html', {"isAdmin" : isAdmin(request), "goods" : getGoods(), "error": getMessage(request)})
        else:
            return render(request, 'createApplication.html', {"isAdmin" : isAdmin(request), "goods": getGoods()})
    elif request.method == "POST":
        data = bodyToJson(request.body.decode('utf-8'))
        data["token"] = request.session["token"]
        r = requests.post(API_URL+"applications/", json=data)
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
            return render(request, 'editApplication.html', {"isAdmin" : isAdmin(request), "application" : getApplication(application_id), "error": getMessage(request)})
        else:
            return render(request, 'editApplication.html', {"isAdmin" : isAdmin(request), "application": getApplication(application_id) })
    elif request.method == "POST":
        data = bodyToJson(request.body.decode('utf-8'))
        data["token"] = request.session["token"]
        r = requests.put(API_URL+"applications/"+str(application_id)+"/", json=data)
        if r.status_code == 400:
            request.session['message'] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/applications/edit/'+str(application_id)+"/")
        else:
            request.session['message'] = "Successfully edited an application"
            return HttpResponseRedirect('/applications/')

@check_is_user
def viewApplication(request, application_id):
    return render(request, 'viewApplication.html', {"isAdmin" : isAdmin(request), "application" : getApplication(application_id)})

@check_is_user
def deleteApplication(request, application_id):
    r = requests.delete(API_URL+"applications/" + str(application_id) + "/")
    request.session['message'] = "Successfully deleted an application"
    return HttpResponseRedirect('/applications/')

@check_is_user
def submitApplication(request, application_id):
    r = requests.get(API_URL + "applications/progress/submitted/" + str(application_id) + "/")
    if r.status_code == 400:
        request.session['message'] = "Error occurred submitting an application"
    else:
        request.session['message'] = "Successfully submitted an application"
    return HttpResponseRedirect('/applications/')
