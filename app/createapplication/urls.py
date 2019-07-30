from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:application_id>/', views.detail, name='detail'),
    path('create', views.createApplication, name='create'),
    path('editapplication/<int:application_id>/', views.editApplication, name='editApplication'),
    path('goods/', views.viewGoods, name='goods'),
    path('editgood/<int:good_id>/', views.editGood, name='editApplication'),
    path('creategood', views.createGood, name='good')
]