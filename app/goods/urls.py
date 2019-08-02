from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.createGood, name='create'),
    path('edit/<int:good_id>/', views.editGood, name='edit'),
    path('view/<int:good_id>/', views.viewGood, name='view'),
    path('delete/<int:good_id>/', views.deleteGood, name='delete')
]