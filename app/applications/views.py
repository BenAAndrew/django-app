from django.shortcuts import render
from app.dataHandler import *
from app.userChecks import check_is_user
from django.http import HttpResponseRedirect


def redirectToLogin(request):
    request.session['message'] = "You must login first"
    return HttpResponseRedirect('/login/')


def index(request):
    if check_is_user(request):
        if "message" in request.session:
            return render(request, 'index.html', {"applications": getApplications(), "message" : getMessage(request)})
        else:
            return render(request, 'index.html', {"applications": getApplications()})
    else:
        return redirectToLogin(request)


def createApplication(request):
    if check_is_user(request):
        if request.method == "GET":
            if "message" in request.session:
                return render(request, 'createApplication.html', {"goods" : getGoods(), "message": getMessage(request)})
            else:
                return render(request, 'createApplication.html', {"goods": getGoods()})
        elif request.method == "POST":
            r = requests.post(API_URL+"application/", json=bodyToJson(request.body.decode('utf-8')))
            if r.status_code == 400:
                request.session['message'] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
                return HttpResponseRedirect('/applications/create/')
            else:
                request.session['message'] = "Successfully created an application"
                return HttpResponseRedirect('/applications/')
    else:
        return redirectToLogin(request)


def editApplication(request, application_id):
    if check_is_user(request):
        if request.method == "GET":
            if "message" in request.session:
                return render(request, 'editApplication.html', { "application" : getApplication(application_id), "message": getMessage(request)})
            else:
                return render(request, 'editApplication.html', {"application": getApplication(application_id) })
        elif request.method == "POST":
            r = requests.put(API_URL+"application/"+str(application_id)+"/", json=bodyToJson(request.body.decode('utf-8')))
            if r.status_code == 400:
                request.session['message'] = handleErrorResponse(json.loads(r.content.decode('utf-8')))
                return HttpResponseRedirect('/applications/edit/'+str(application_id)+"/")
            else:
                request.session['message'] = "Successfully edited an application"
                return HttpResponseRedirect('/applications/')
    else:
        return redirectToLogin(request)


def viewApplication(request, application_id):
    if check_is_user(request):
        return render(request, 'viewApplication.html', { "application" : getApplication(application_id) })
    else:
        return redirectToLogin(request)


def deleteApplication(request, application_id):
    if check_is_user(request):
        r = requests.delete(API_URL+"application/" + str(application_id) + "/")
        request.session['message'] = "Successfully deleted an application"
        return HttpResponseRedirect('/applications/')
    else:
        return redirectToLogin(request)


def submitApplication(request, application_id):
    if check_is_user(request):
        r = requests.get(API_URL + "application/submit/" + str(application_id) + "/")
        if r.status_code == 400:
            request.session['message'] = "Error occurred submitting an application"
        else:
            request.session['message'] = "Successfully submitted an application"
        return HttpResponseRedirect('/applications/')
    else:
        return redirectToLogin(request)


def resubmitApplication(request, application_id):
    if check_is_user(request):
        r = requests.get(API_URL + "application/resubmit/" + str(application_id) + "/")
        if r.status_code == 400:
            request.session['message'] = "Error occurred submitting an application"
        else:
            request.session['message'] = "Successfully submitted an application"
        return HttpResponseRedirect('/applications/')
    else:
        return redirectToLogin(request)
