import json
from django.http import JsonResponse, HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser
from .models import Good
from .serializers import GoodSerializer
from users.views import TokenHandler

tokenHandler = TokenHandler()

class GoodsView(ListCreateAPIView):
    serializer_class = GoodSerializer
    model = Good
    queryset = Good.objects.all()

    def get(self, request):
        user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
        goods = Good.objects.all().filter(user=user_id)
        serializer = GoodSerializer(goods, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        data["user"] = tokenHandler.get_user_id_token(request.COOKIES["token"])
        serializer = GoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class GoodView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoodSerializer
    model = Good
    queryset = Good.objects.all()

    def get(self, request, good_id):
        try:
            user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
            good = Good.objects.get(pk=good_id, user=user_id)
            serializer = GoodSerializer(good, many=False)
            return JsonResponse(serializer.data, safe=False)
        except Good.DoesNotExist:
            return HttpResponse(status=404)

    def put(self, request, good_id):
        try:
            user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
            good = Good.objects.get(pk=good_id, user=user_id)
            data = JSONParser().parse(request)
            data["user"] = user_id
            serializer = GoodSerializer(good, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except Good.DoesNotExist:
            return HttpResponse(status=404)

    def delete(self, request, good_id):
        try:
            user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
            good = Good.objects.get(pk=good_id, user=user_id)
            good.delete()
            return HttpResponse(status=204)
        except Good.DoesNotExist:
            return HttpResponse(status=404)
