from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_good, name='create'),
    path('edit/<int:good_id>/', views.edit_good, name='edit'),
    path('view/<int:good_id>/', views.view_good, name='view'),
    path('delete/<int:good_id>/', views.delete_good, name='delete')
]