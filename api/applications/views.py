from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser


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