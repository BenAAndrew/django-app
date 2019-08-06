from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='users'),
    path('create/', views.create, name='create'),
]
