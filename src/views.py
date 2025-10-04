from urllib import request
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("¡Hola! Esta es la primera página web con Django.")

def driver_registration(request):
    return render(request, 'driver_registration.html')
