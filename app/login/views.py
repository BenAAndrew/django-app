from django.shortcuts import render
from app.dataHandler import *
from django.http import HttpResponse

def index(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        r = requests.post(API_URL + "login/", json=bodyToJson(request.body.decode('utf-8')))
        if r.status_code == 200:
            request.session['token'] = json.loads(r.content.decode('utf-8'))["token"]
            return HttpResponse("Session")
        else:
            return HttpResponse("Not found")

def create(request):
    if request.method == "GET":
        return render(request, 'createuser.html')
    elif request.method == "POST":
        r = requests.post(API_URL + "login/create/", json=bodyToJson(request.body.decode('utf-8')))
        return render(request, 'createuser.html')