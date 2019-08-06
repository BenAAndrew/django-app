from django.urls import path
from . import views

urlpatterns = [
    path('', views.good_list, name="goods"),
    path('<int:good_id>/', views.good_detail, name="good")
]
