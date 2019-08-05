from django.shortcuts import render
from app.dataHandler import *
from app.userChecks import check_is_admin
from django.http import HttpResponseRedirect

def index(request):
    if check_is_admin(request):
        return render(request, 'admin.html', {"applications": getApplications()})
    else:
        return HttpResponseRedirect('/applications/')

def review(request, application_id):
    return render(request, 'reviewApplication.html', {"application": getApplication(application_id)})


def accept(request, application_id):
    r = requests.get(API_URL + "application/accept/" + str(application_id) + "/")
    if r.status_code == 400:
        return render(request, 'admin.html', {"applications": getApplications()})
    else:
        return render(request, 'admin.html',
                      {"applications": getApplications(), "message": "Successfully accepted an application"})


def reject(request, application_id):
    r = requests.get(API_URL + "application/reject/" + str(application_id) + "/")
    if r.status_code == 400:
        return render(request, 'admin.html', {"applications": getApplications()})
    else:
        return render(request, 'admin.html',
                      {"applications": getApplications(), "message": "Successfully rejected an application"})