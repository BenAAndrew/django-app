from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_application, name='create'),
    path('edit/<int:application_id>/', views.edit_application, name='editApplication'),
    path('view/<int:application_id>/', views.view_application, name='viewApplication'),
    path('delete/<int:application_id>/', views.delete_application, name='deleteApplication'),
    path('submit/<int:application_id>/', views.submit_application, name='submitApplication'),
]