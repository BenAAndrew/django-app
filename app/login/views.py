from django.shortcuts import render
from app.dataHandler import *
from django.http import HttpResponseRedirect

def index(request):
    if request.method == "GET":
        if "message" in request.session:
            return render(request, 'login.html', {"message" : getMessage(request)})
        else:
            return render(request, 'login.html')
    elif request.method == "POST":
        r = requests.post(API_URL + "login/", json=bodyToJson(request.body.decode('utf-8')))
        if r.status_code == 200:
            request.session['token'] = json.loads(r.content.decode('utf-8'))["token"]
            return HttpResponseRedirect('/applications/')
        else:
            request.session['message'] = "User not found"
            return HttpResponseRedirect('/login/')

def create(request):
    if request.method == "GET":
        return render(request, 'createuser.html')
    elif request.method == "POST":
        r = requests.post(API_URL + "login/create/", json=bodyToJson(request.body.decode('utf-8')))
        return rHttpResponseRedirect('/login/create/')

def logout(request):
    request.session['token'] = None
    return HttpResponseRedirect('/login/')