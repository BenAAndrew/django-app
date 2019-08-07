from django.shortcuts import render
from app.dataHandler import *
from app.userChecks import check_is_admin, isAdmin
from django.http import HttpResponseRedirect


@check_is_admin
def index(request):
    return render(request, 'admin.html', {"isAdmin" : isAdmin(request), "applications": getApplications()})


@check_is_admin
def review(request, application_id):
    return render(request, 'reviewApplication.html', {"isAdmin" : isAdmin(request), "application": getApplication(application_id)})


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
