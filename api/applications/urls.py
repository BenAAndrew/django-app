from django.urls import path
from . import views

urlpatterns = [
    path('', views.application_list, name='index'),
    path('<int:application_id>/', views.application_detail, name='detail'),
    path('good/', views.good_list, name="goods"),
    path('good/<int:good_id>/', views.good_detail, name="goods"),
]
