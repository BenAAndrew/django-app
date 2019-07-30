from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response

from .models import Application
from datetime import datetime

def index(request):
    return render(request, 'createapplication/index.html', { "applications" : Application.objects.order_by('date') })

def detail(request, application_id):
    return HttpResponse("You're looking at question %s." % application_id)

def create(request):
    return render(request, 'createapplication/create.html')

def add(request):
    app = Application(name=request.POST['name'], date=datetime.now(), destination=request.POST['destination'])
    app.save()
    return HttpResponse(app)

def application(request, application_id):
    app = Application.objects.filter(id=application_id).values()
    return Response({'application': app}, 200)
