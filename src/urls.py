from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
     path('driver-registration/', views.driver_registration, name='driver_registration'),
]
