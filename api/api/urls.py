"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import viewsets, schemas
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_swagger.views import get_swagger_view

from applications.models import Application
from applications.serializers import ApplicationSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    """
    request: return applications
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    model = Application

    @action(detail='blah')
    def set_price(self, request, pk):
        """An example action to on the ViewSet."""
        return Response('20$')

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('applications/', include('applications.urls')),
    path('goods/', include('goods.urls')),
    path('users/', include('users.urls')),
    #path('admin/', admin.site.urls),
    path('swagger/', TemplateView.as_view(template_name='swagger.html'), name='swagger-ui'),
    path('docs/', schema_view),
]
