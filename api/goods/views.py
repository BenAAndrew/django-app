import json
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from .models import Good
from .serializers import GoodSerializer


def good_list(request):
    if request.method == 'GET':
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
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
