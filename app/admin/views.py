from django.shortcuts import render
from app.userChecks import check_is_admin, isAdmin
from django.http import HttpResponseRedirect
from applications.views import getApplication, progressToProgressPercent
from app.tools import *


def getApplications(request):
    applications = decode_request(requests.get("http://127.0.0.1:8001/admin/", cookies=request.COOKIES))
    for i in range(0, len(applications)):
        applications[i]["progress_percent"] = progressToProgressPercent(applications[i])
        applications[i]["progress"] = applications[i]["progress"].capitalize()
    return applications


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
