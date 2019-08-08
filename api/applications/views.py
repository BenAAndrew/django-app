import json
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import GenericAPIView
from .models import Application, Good
from .serializers import ApplicationSerializer
from drf_yasg.utils import swagger_auto_schema
from users.views import TokenHandler

tokenHandler = TokenHandler()

class ApplicationsView(GenericAPIView):
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()

    @swagger_auto_schema(operation_description="Get all applications")
    def get(self, request):
        user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
        applications = Application.objects.all().filter(user=user_id)
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request):
        data = json.loads(request.body)
        data["user"] = tokenHandler.get_user_id_token(data["token"])
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ApplicationView(GenericAPIView):
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()

    @swagger_auto_schema(operation_description="Fetch an application of given ID")
    def get(self, request, application_id):
        try:
            user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
            application = Application.objects.get(pk=application_id, user=user_id)
            serializer = ApplicationSerializer(application, many=False)
            return JsonResponse(serializer.data, safe=False)
        except Application.DoesNotExist:
            return HttpResponse(status=404)

    def put(self, request, application_id):
        try:
            user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
            application = Application.objects.get(pk=application_id, user=user_id)
            data = json.loads(request.body)
            data["user"] = tokenHandler.get_user_id_token(data["token"])
            serializer = ApplicationSerializer(application, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except Application.DoesNotExist:
            return HttpResponse(status=404)

    def delete(self, request, application_id):
        try:
            user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
            application = Application.objects.get(pk=application_id, user=user_id)
            application.delete()
            return HttpResponse(status=204)
        except Application.DoesNotExist:
            return HttpResponse(status=404)


class ApplicationProgressView(GenericAPIView):
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()

    def check_progress_update(self, new_progress, old_progress):
        if new_progress == "submitted":
            return old_progress in ["draft","declined"]
        elif new_progress in ["approved", "declined"]:
            return old_progress == "submitted"
        else:
            return False

    def get(self, request, application_id, new_progress):
        try:
            #user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
            application = Application.objects.get(pk=application_id)
            print(application.progress + " => " + new_progress)
            if self.check_progress_update(new_progress, application.progress):
                application.progress = new_progress
                application.save()
                return HttpResponse(status=204)
            return HttpResponse(status=404)
        except Application.DoesNotExist:
            return HttpResponse(status=404)
