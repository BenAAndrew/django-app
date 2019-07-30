from django.urls import path
from . import views

urlpatterns = [
    path('', views.application, name='index'),
    path('<int:application_id>/', views.application, name='detail')
]