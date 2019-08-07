from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='users'),
    path('create/', views.CreateUserView.as_view(), name='create'),
]
