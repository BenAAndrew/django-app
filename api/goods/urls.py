from django.urls import path
from . import views

urlpatterns = [
    path('', views.GoodsView.as_view(), name="goods"),
    path('<int:good_id>/', views.GoodView.as_view(), name="good")
]
