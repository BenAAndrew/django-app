from django.http import JsonResponse
from rest_framework.generics import GenericAPIView

from applications.models import Application
from applications.serializers import ApplicationSerializer
from users.views import TokenHandler

tokenHandler = TokenHandler()

class AdminView(GenericAPIView):
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()

    def get(self, request):
        user_id = tokenHandler.get_user_id_token(request.COOKIES["token"])
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)