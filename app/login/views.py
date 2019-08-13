from django.shortcuts import render
from app.tools import form_body_to_json, get_message_or_error
from django.http import HttpResponseRedirect
from app.userChecks import is_admin
from app.apiRequest import post_request
import json


def index(request):
    if request.method == "GET":
        msg = get_message_or_error(request)
        if msg:
            return render(request, 'login.html', msg)
        else:
            return render(request, 'login.html')
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        r = post_request(request, "users", data)
        if r.status_code == 200:
            if is_admin(request):
                response = HttpResponseRedirect('/admin/')
            else:
                response = HttpResponseRedirect('/applications/')
            response.set_cookie('token', json.loads(r.content.decode('utf-8'))["token"])
            return response
        else:
            request.session['error'] = "User not found"
            return HttpResponseRedirect('/login/')


def create(request):
    if request.method == "GET":
        return render(request, 'createuser.html')
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        post_request(request, "create_account", data)
        request.session['message'] = "User created"
        return HttpResponseRedirect('/login/')


def logout():
    response = HttpResponseRedirect('/login/')
    response.set_cookie('token', None)
    return response
