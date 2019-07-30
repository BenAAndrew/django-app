from django.urls import path
from . import views

urlpatterns = [
    path('', views.application_list, name='index'),
    path('<int:application_id>/', views.application_detail, name='detail')
]