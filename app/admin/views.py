from django.shortcuts import render
from app.dataHandler import *


def index(request):
    return render(request, 'admin.html', {"applications": getApplications()})


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