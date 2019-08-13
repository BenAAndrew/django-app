from django.shortcuts import render
from app.userChecks import check_is_admin, is_admin
from django.http import HttpResponseRedirect
from applications.views import add_progress_to_applications
from app.apiRequest import get_request


def get_admin_applications(request):
    applications = get_request(request, "admin", data_only=True)
    return add_progress_to_applications(applications)


def get_admin_goods(request, application):
    ids = application["goods"]
    goods = get_request(request, "admin_goods", data_only=True)
    final = list()
    for i in range(0, len(goods)):
        if goods[i]["id"] in ids:
            final.append(goods[i])
    return final


def get_admin_application(id, request):
    application = get_request(request, "admin", url_extension=str(id)+"/", data_only=True)
    application["goods"] = get_admin_goods(request, application)
    return application


@check_is_admin
def index(request):
    return render(request, 'admin.html', {"isAdmin": is_admin(request),
                                          "applications": get_admin_applications(request)})


@check_is_admin
def review(request, application_id):
    return render(request, 'reviewApplication.html', {"isAdmin": is_admin(request),
                                                      "application": get_admin_application(application_id, request)})


@check_is_admin
def accept(request, application_id):
    r = get_request(request, "approve", url_extension=str(application_id)+"/")
    if r.status_code == 400:
        request.session['error'] = "Error occurred when accepting application"
    else:
        request.session['message'] = "Successfully accepted an application"
    return HttpResponseRedirect('/admin/')


@check_is_admin
def reject(request, application_id):
    r = get_request(request, "decline", url_extension=str(application_id) + "/")
    if r.status_code == 400:
        request.session['error'] = "Error occurred when rejecting application"
    else:
        request.session['message'] = "Successfully rejected an application"
    return HttpResponseRedirect('/admin/')
