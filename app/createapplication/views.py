from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Application
from datetime import datetime
from .serializers import ApplicationSerializer

def index(request):
    return render(request, 'createapplication/index.html', { "applications" : Application.objects.order_by('date') })

def detail(request, application_id):
    return HttpResponse("You're looking at question %s." % application_id)

def create(request):
    if request.method == "GET":
        return render(request, 'createapplication/create.html')
    elif request.method == "POST":
        return HttpResponse("ABC")