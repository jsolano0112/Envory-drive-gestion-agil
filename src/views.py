from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def index(request):
    return render(request, 'index.html')

def inicio(request):
    return HttpResponse("¡Hola! Esta es la primera página web con Django.")

def driver_registration(request):
    return render(request, 'driver_registration.html')

def login(request):
    return render(request, 'login.html')
