from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser

from .models import Application

def index(request):
    return render(request, 'createapplication/index.html', { "applications" : Application.objects.order_by('date') })

def detail(request, application_id):
    return HttpResponse("You're looking at question %s." % application_id)

def create(request):
    if request.method == "GET":
        return render(request, 'createapplication/create.html')
    elif request.method == "POST":
        parsed = JSONParser().parse(request)
        request.post("http://127.0.0.1:8001/application", data=parsed)
        return HttpResponse("SENT")

