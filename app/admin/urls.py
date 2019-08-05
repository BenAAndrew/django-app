from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('review/<int:application_id>/', views.review, name='review'),
    path('accept/<int:application_id>/', views.accept, name='accept'),
    path('reject/<int:application_id>/', views.reject, name='reject'),
]