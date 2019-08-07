import json
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.generics import GenericAPIView
from .models import Application, Good
from .serializers import ApplicationSerializer


class ApplicationsView(GenericAPIView):
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()

    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request):
        values = json.loads(request.body)
        serializer = ApplicationSerializer(data=values)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def process_application(application_id, inner_func):
    try:
        application = Application.objects.get(pk=application_id)
        return inner_func(application)
    except Application.DoesNotExist:
        return HttpResponse(status=404)

class ApplicationView(GenericAPIView):
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()

    def get(self, request, application_id):
        def get_application(application):
            serializer = ApplicationSerializer(application, many=False)
            return JsonResponse(serializer.data, safe=False)
        return process_application(application_id, get_application)

    def put(self, request, application_id):
        def put_application(application):
            data = json.loads(request.body)
            serializer = ApplicationSerializer(application, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        return process_application(application_id, put_application)

    def delete(self, request, application_id):
        def delete_application(application):
            application.delete()
            return HttpResponse(status=204)
        return process_application(application_id, delete_application)

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
        def put_application(application):
            print(str(application_id))
            print(application.progress + " => " + new_progress)
            if self.check_progress_update(new_progress, application.progress):
                application.progress = new_progress
                application.save()
                return HttpResponse(status=204)
            return HttpResponse(status=404)
        return process_application(application_id, put_application)
