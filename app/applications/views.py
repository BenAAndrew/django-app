from django.shortcuts import render
from app.userChecks import check_is_user, is_admin
from django.http import HttpResponseRedirect
from goods.views import getGoods, getGoodsNames, getGoodsSelected
from app.tools import form_body_to_json, handle_error_response, get_message
from app.apiRequest import get_request, post_request, put_request, delete_request

progress = ['draft', 'submitted', 'processing', 'approved']


def progress_to_progress_percent(application):
    state = application["progress"]
    if state == 'declined':
        return 5
    else:
        return (progress.index(state)+1) * 25


def add_progress_to_applications(applications):
    for i in range(0, len(applications)):
        applications[i]["progress_percent"] = progress_to_progress_percent(applications[i])
        applications[i]["progress"] = applications[i]["progress"].capitalize()
    return applications


def get_applications(request):
    applications = get_request(request, "applications", data_only=True)
    return add_progress_to_applications(applications)


def get_application(id, request):
    application = get_request(request, "applications", url_extension=str(id)+"/", data_only=True)
    application["goods"] = getGoodsNames(application["goods"], request)
    application["goods"] = getGoodsSelected([good["id"] for good in application["goods"]], request)
    return application


@check_is_user
def index(request):
    data = {"isAdmin" : is_admin(request), "applications": get_applications(request)}
    if "message" in request.session:
        data["message"] = get_message(request)
    return render(request, 'index.html', data)


@check_is_user
def createApplication(request):
    if request.method == "GET":
        data = {"isAdmin" : is_admin(request), "goods" : getGoods(request)}
        if "message" in request.session:
            data["error"] = get_message(request)
        return render(request, 'createApplication.html', data)
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        r = post_request(request, "applications", data)
        if r.status_code == 400:
            request.session['message'] = handle_error_response(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/applications/create/')
        else:
            request.session['message'] = "Successfully created an application"
            return HttpResponseRedirect('/applications/')


@check_is_user
def editApplication(request, application_id):
    if request.method == "GET":
        data = {"isAdmin" : is_admin(request), "application": get_application(application_id, request)}
        if "message" in request.session:
            data["error"] = get_message(request)
        return render(request, 'editApplication.html', data)
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        r = put_request(request, "applications", data, url_extension=str(application_id)+"/")
        if r.status_code == 400:
            request.session['message'] = handle_error_response(json.loads(r.content.decode('utf-8')))
            return HttpResponseRedirect('/applications/edit/'+str(application_id)+"/")
        else:
            request.session['message'] = "Successfully edited an application"
            return HttpResponseRedirect('/applications/')


@check_is_user
def viewApplication(request, application_id):
    return render(request, 'viewApplication.html', {"isAdmin" : is_admin(request), "application" : get_application(application_id, request)})


@check_is_user
def deleteApplication(request, application_id):
    r = delete_request(request, "applications", url_extension=str(application_id)+"/")
    request.session['message'] = "Successfully deleted an application"
    return HttpResponseRedirect('/applications/')


@check_is_user
def submitApplication(request, application_id):
    r = get_request(request, "submit", url_extension=str(application_id)+"/")
    if r.status_code == 400:
        request.session['message'] = "Error occurred submitting an application"
    else:
        request.session['message'] = "Successfully submitted an application"
    return HttpResponseRedirect('/applications/')
