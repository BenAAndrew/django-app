from django.urls import path
from . import views

urlpatterns = [
    path('', views.application_list, name='index'),
    path('<int:application_id>/', views.application_detail, name='detail'),
    path('good/', views.good_list, name="goods"),
    path('good/<int:good_id>/', views.good_detail, name="goods"),
    path('submit/<int:application_id>/', views.submit_application, name='submit'),
    path('accept/<int:application_id>/', views.accept_application, name='accepted'),
    path('reject/<int:application_id>/', views.reject_application, name='rejected'),
    path('resubmit/<int:application_id>/', views.resubmit_application, name='rejected'),
]
