from django.urls import path
from . import views


urlpatterns = [
    # Rutas existentes
    path('', views.inicio, name='inicio'),
    path('registro-conductores/', views.driver_registration, name='driver_registration'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    # ====================================
    # MÓDULO: REGISTRO DE CLIENTES
    # ====================================
    # Vista del formulario
    path('registro-cliente/', views.client_registration, name='client_registration'),
    
    # API Endpoints
    path('api/clientes/registro/', views.client_registration_api, name='client_registration_api'),
    path('api/clientes/', views.client_list_api, name='client_list_api'),
    path('api/companias/', views.companies_list_api, name='companies_list_api'),
    
    # ====================================
    # MÓDULO: REGISTRO DE CONDUCTORES
    # ====================================
    # API Endpoints para conductores
    path('api/conductores/registro/', views.driver_registration_api, name='driver_registration_api'),
    path('api/conductores/', views.driver_list_api, name='driver_list_api'),
]
