import json
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Application, Good
from .serializers import ApplicationSerializer

def application_detail(request, application_id):
    try:
        application = Application.objects.get(pk=application_id)
    except:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ApplicationSerializer(application, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        serializer = ApplicationSerializer(application, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        application.delete()
        return HttpResponse(status=204)

def application_list(request):
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    elif request.method == 'POST':
        values = json.loads(request.body)
        serializer = ApplicationSerializer(data=values)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def process_application(application_id, current_state, new_state):
    try:
        application = Application.objects.get(pk=application_id)
    except:
        return HttpResponse(status=404)
    if application.progress == current_state:
        application.progress = new_state
        application.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)

def submit_application(request, application_id):
    return process_application(application_id, 'draft','submitted')

def accept_application(request, application_id):
    return process_application(application_id, 'submitted', 'approved')

def reject_application(request, application_id):
    return process_application(application_id, 'submitted', 'declined')

def resubmit_application(request, application_id):
    return process_application(application_id, 'declined', 'submitted')