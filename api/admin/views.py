from django.http import JsonResponse, HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView

from applications.models import Application
from applications.serializers import ApplicationSerializer
from goods.models import Good
from goods.serializers import GoodSerializer
from users.views import TokenHandler

tokenHandler = TokenHandler()

def isAdmin(*args):
    request = args[1]
    try:
        token = tokenHandler.decode_token(request.COOKIES["token"])
        return token["admin"]
    except:
        pass
    return False

def check_admin(input_func):
    def admin(*args, **kwargs):
        if isAdmin(*args):
            return input_func(*args, **kwargs)
        else:
            return HttpResponse(status=401)
    return admin

class AdminApplicationsView(ListAPIView):
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()

    @check_admin
    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

class AdminApplicationView(RetrieveAPIView):
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()

    @check_admin
    def get(self, request, application_id):
        try:
            application = Application.objects.get(pk=application_id)
            serializer = ApplicationSerializer(application, many=False)
            return JsonResponse(serializer.data, safe=False)
        except Application.DoesNotExist:
            return HttpResponse(status=404)

class AdminGoodsView(ListAPIView):
    serializer_class = GoodSerializer
    model = Good
    queryset = Good.objects.all()

    @check_admin
    def get(self, request):
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return JsonResponse(serializer.data, safe=False)

class AdminGoodView(RetrieveAPIView):
    serializer_class = GoodSerializer
    model = Good
    queryset = Good.objects.all()

    @check_admin
    def get(self, request, good_id):
        try:
            good = Good.objects.get(pk=good_id)
            serializer = GoodSerializer(good, many=False)
            return JsonResponse(serializer.data, safe=False)
        except Good.DoesNotExist:
            return HttpResponse(status=404)