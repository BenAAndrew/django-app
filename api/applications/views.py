import json
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.generics import GenericAPIView
from .models import Application, Good
from .serializers import ApplicationSerializer


class ApplicationsView(GenericAPIView):
    serializer_class = ApplicationSerializer

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


class ApplicationView(GenericAPIView):
    serializer_class = ApplicationSerializer

    def process_application(self, application_id, inner_func):
        try:
            application = Application.objects.get(pk=application_id)
            return inner_func(application)
        except Application.DoesNotExist:
            return HttpResponse(status=404)

    def get(self, request, application_id):
        def get_application(application):
            serializer = ApplicationSerializer(application, many=False)
            return JsonResponse(serializer.data, safe=False)
        return self.process_application(application_id, get_application)

    def put(self, request, application_id):
        def put_application(application):
            data = json.loads(request.body)
            serializer = ApplicationSerializer(application, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        return self.process_application(application_id, put_application)

    def delete(self, request, application_id):
        def delete_application(application):
            application.delete()
            return HttpResponse(status=204)
        return self.process_application(application_id, delete_application)


def application_progress(application_id, current_state, new_state):
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
    return application_progress(application_id, 'draft','submitted')


def accept_application(request, application_id):
    return application_progress(application_id, 'submitted', 'approved')


def reject_application(request, application_id):
    return application_progress(application_id, 'submitted', 'declined')


def resubmit_application(request, application_id):
    return application_progress(application_id, 'declined', 'submitted')
