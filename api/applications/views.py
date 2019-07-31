from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser

from .models import Application, Good
from .serializers import ApplicationSerializer, GoodSerializer

def application_detail(request, application_id):
    try:
        application = Application.objects.get(pk=application_id)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ApplicationSerializer(application, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = ApplicationSerializer(application, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        application.delete()
        return HttpResponse(status=204)

def bodyToJson(body):
    elements = body.split("&")
    values = dict()
    for element in elements:
        data = element.split("=")
        if data[0] in values:
            if not isinstance(values[data[0]], list):
                copy = values[data[0]]
                values[data[0]] = list()
                values[data[0]].append(copy)
            values[data[0]].append(data[1])
        else:
            values[data[0]] = data[1]
    return values

def application_list(request):
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    elif request.method == 'POST':
        values = bodyToJson(request.body.decode('utf-8'))
        goods = values.pop('goods', None)
        serializer = ApplicationSerializer(data=values)
        if serializer.is_valid():
            serializer.save()
            application = Application.objects.all()[Application.objects.count() - 1]
            for good in goods:
                application.goods.add(Good.objects.get(id=good))
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def good_list(request):
    if request.method == 'GET':
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = bodyToJson(request.body.decode('utf-8'))
        serializer = GoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def good_detail(request, good_id):
    try:
        good = Good.objects.get(pk=good_id)
    except:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = GoodSerializer(good, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = GoodSerializer(good, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        good.delete()
        return HttpResponse(status=204)
