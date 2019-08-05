from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.createApplication, name='create'),
    path('edit/<int:application_id>/', views.editApplication, name='editApplication'),
    path('view/<int:application_id>/', views.viewApplication, name='viewApplication'),
    path('delete/<int:application_id>/', views.deleteApplication, name='deleteApplication'),
    path('submit/<int:application_id>/', views.submitApplication, name='submitApplication'),
]