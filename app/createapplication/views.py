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
    return render(request, 'createapplication/create.html')

def add(request):
    app = Application(name=request.POST['name'], date=datetime.now(), destination=request.POST['destination'])
    app.save()
    return HttpResponse(app)

def application(request, application_id):
    try:
        application = Application.objects(pk=application_id)
    except Application.DoesNotExit:
        return HttpResponse(status=404)

def application(request):
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
