from django.shortcuts import render
from app.tools import *
from django.http import HttpResponseRedirect
from app.userChecks import isAdmin
from app.apiRequest import post_request

def index(request):
    if request.method == "GET":
        if "message" in request.session:
            return render(request, 'login.html', {"error" : get_message(request)})
        else:
            return render(request, 'login.html')
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        r = post_request(request, "users", data)
        if r.status_code == 200:
            request.session['token'] = json.loads(r.content.decode('utf-8'))["token"]
            if isAdmin(request):
                response = HttpResponseRedirect('/admin/')
            else:
                response = HttpResponseRedirect('/applications/')
            response.set_cookie('token', json.loads(r.content.decode('utf-8'))["token"])
            return response
        else:
            request.session['message'] = "User not found"
            return HttpResponseRedirect('/login/')

def create(request):
    if request.method == "GET":
        return render(request, 'createuser.html')
    elif request.method == "POST":
        data = form_body_to_json(request.body.decode('utf-8'))
        r = post_request(request, "create_account", data)
        return HttpResponseRedirect('/login/create/')

def logout(request):
    request.session['token'] = None
    return HttpResponseRedirect('/login/')