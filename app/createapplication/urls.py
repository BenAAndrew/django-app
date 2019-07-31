from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:application_id>/', views.detail, name='detail'),
    path('create/', views.createApplication, name='create'),
    path('editapplication/<int:application_id>/', views.editApplication, name='editApplication'),
    path('viewapplication/<int:application_id>/', views.viewApplication, name='viewApplication'),
    path('deleteapplication/<int:application_id>/', views.deleteApplication, name='deleteApplication'),
    path('goods/', views.viewGoods, name='goods'),
    path('editgood/<int:good_id>/', views.editGood, name='editGood'),
    path('viewgood/<int:good_id>/', views.viewGood, name='viewGood'),
    path('deletegood/<int:good_id>/', views.deleteGood, name='deleteGood'),
    path('creategood/', views.createGood, name='good')
]