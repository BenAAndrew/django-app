from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminApplicationsView.as_view(), name="admin"),
    path('<int:application_id>/', views.AdminApplicationView.as_view(), name='detail'),
    path('goods/', views.AdminGoodsView.as_view(), name='goods'),
    path('goods/<int:good_id>/', views.AdminGoodView.as_view(), name='good')
]
