from django.shortcuts import render
from app.dataHandler import *


def index(request):
    return render(request, 'admin.html', {"applications": getApplications()})