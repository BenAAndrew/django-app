from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApplicationsView.as_view(), name='index'),
    path('<int:application_id>/', views.ApplicationView.as_view(), name='detail'),
    path('submit/<int:application_id>/', views.submit_application, name='submit'),
    path('accept/<int:application_id>/', views.accept_application, name='accepted'),
    path('reject/<int:application_id>/', views.reject_application, name='rejected'),
    path('resubmit/<int:application_id>/', views.resubmit_application, name='rejected')
]
