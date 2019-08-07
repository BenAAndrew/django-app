import json
from django.http import JsonResponse, HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from .models import Good
from .serializers import GoodSerializer


class GoodsView(GenericAPIView):
    serializer_class = GoodSerializer
    model = Good
    queryset = Good.objects.all()

    def get(self, request):
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        serializer = GoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class GoodView(GenericAPIView):
    serializer_class = GoodSerializer
    model = Good
    queryset = Good.objects.all()

    def get(self, request, good_id):
        try:
            good = Good.objects.get(pk=good_id)
            serializer = GoodSerializer(good, many=False)
            return JsonResponse(serializer.data, safe=False)
        except Good.DoesNotExist:
            return HttpResponse(status=404)

    def put(self, request, good_id):
        try:
            good = Good.objects.get(pk=good_id)
            data = JSONParser().parse(request)
            serializer = GoodSerializer(good, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except Good.DoesNotExist:
            return HttpResponse(status=404)

    def delete(self, request, good_id):
        try:
            good = Good.objects.get(pk=good_id)
            good.delete()
            return HttpResponse(status=204)
        except Good.DoesNotExist:
            return HttpResponse(status=404)
