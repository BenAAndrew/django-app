from django.shortcuts import render
from app.dataHandler import *
from app.userChecks import check_is_admin
from django.http import HttpResponseRedirect


@check_is_admin
def index(request):
    return render(request, 'admin.html', {"applications": getApplications()})


@check_is_admin
def review(request, application_id):
    return render(request, 'reviewApplication.html', {"application": getApplication(application_id)})


@check_is_admin
def accept(request, application_id):
    r = requests.get(API_URL + "application/accept/" + str(application_id) + "/")
    if r.status_code == 400:
        request.session['message'] = "Error occurred when accepting application"
    else:
        request.session['message'] = "Successfully accepted an application"
    HttpResponseRedirect('/admin/')


@check_is_admin
def reject(request, application_id):
    r = requests.get(API_URL + "application/reject/" + str(application_id) + "/")
    if r.status_code == 400:
        request.session['message'] = "Error occurred when rejecting application"
    else:
        request.session['message'] = "Successfully rejected an application"
    HttpResponseRedirect('/admin/')
