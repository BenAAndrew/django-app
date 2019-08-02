from django.shortcuts import render
from app.dataHandler import *

def index(request):
    return render(request, 'index.html', {"applications": getApplications()})


def createApplication(request):
    if request.method == "GET":
        return render(request, 'createApplication.html', { "goods" : getGoods() })
    elif request.method == "POST":
        r = requests.post(API_URL+"application/", json=bodyToJson(request.body.decode('utf-8')))
        if r.status_code == 400:
            errorResponse = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return render(request, 'createApplication.html',
                          {"goods": getGoods() , "message" : errorResponse})
        else:
            return render(request, 'index.html',
                      { "applications" : getApplications(), "message" : "Successfully created an application" })


def editApplication(request, application_id):
    if request.method == "GET":
        print(getApplication(application_id))
        return render(request, 'editApplication.html', { "application" : getApplication(application_id) })
    elif request.method == "POST":
        r = requests.put(API_URL+"/application/"+str(application_id)+"/", json=bodyToJson(request.body.decode('utf-8')))
        if r.status_code == 400:
            errorResponse = handleErrorResponse(json.loads(r.content.decode('utf-8')))
            return render(request, 'editApplication.html',
                          { "application" : getApplication(application_id), "message": errorResponse })
        else:
            return render(request, 'index.html',
                      { "applications" : getApplications(), "message" : "Successfully edited an application" })


def viewApplication(request, application_id):
    print(getApplication(application_id))
    return render(request, 'viewApplication.html', { "application" : getApplication(application_id) })


def deleteApplication(request, application_id):
    r = requests.delete(API_URL+"application/" + str(application_id) + "/")
    return render(request, 'index.html',
                  { "applications" : getApplications(), "message" : "Successfully deleted an application" })


def submitApplication(request, application_id):
    print("SUBMIT")
    r = requests.get(API_URL + "application/submit/" + str(application_id) + "/")
    print(r.status_code)
    return render(request, 'index.html',
                  {"applications": getApplications(), "message": "Successfully submitted an application"})
