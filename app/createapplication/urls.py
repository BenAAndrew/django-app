from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:application_id>/', views.detail, name='detail'),
    path('create', views.createApplication, name='create'),
    path('creategood', views.createGood, name='good')
]