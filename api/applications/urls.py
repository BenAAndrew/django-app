from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApplicationsView.as_view(), name='index'),
    path('<int:application_id>/', views.ApplicationView.as_view(), name='detail'),
    path('progress/<str:new_progress>/<int:application_id>/', views.ApplicationProgressView.as_view(), name='progress')
]
