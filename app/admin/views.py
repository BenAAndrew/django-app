from django.shortcuts import render
from app.dataHandler import *
from app.userChecks import check_is_admin
from django.http import HttpResponseRedirect

def redirectToHome():
    request.session['message'] = "You do not have rights to access that page"
    return HttpResponseRedirect('/applications/')

def index(request):
    if check_is_admin(request):
        return render(request, 'admin.html', {"applications": getApplications()})
    else:
        redirectToHome()

def review(request, application_id):
    if check_is_admin(request):
        return render(request, 'reviewApplication.html', {"application": getApplication(application_id)})
    else:
        redirectToHome()


def accept(request, application_id):
    if check_is_admin(request):
        r = requests.get(API_URL + "application/accept/" + str(application_id) + "/")
        if r.status_code == 400:
            return render(request, 'admin.html', {"applications": getApplications()})
        else:
            return render(request, 'admin.html',
                          {"applications": getApplications(), "message": "Successfully accepted an application"})
    else:
        redirectToHome()


def reject(request, application_id):
    r = requests.get(API_URL + "application/reject/" + str(application_id) + "/")
    if r.status_code == 400:
        return render(request, 'admin.html', {"applications": getApplications()})
    else:
        return render(request, 'admin.html',
                      {"applications": getApplications(), "message": "Successfully rejected an application"})