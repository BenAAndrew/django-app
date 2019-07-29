from django.shortcuts import render
from .models import Application

def index(request):
    return render(request, 'createapplication/index.html', { "applications" : Application.objects.order_by('date') })