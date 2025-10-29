from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import driver_history_views

urlpatterns = [
    # ====================================
    # RUTAS PRINCIPALES
    # ====================================
    path('', views.inicio, name='inicio'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),

    # ====================================
    # MÓDULO: REGISTRO DE CLIENTES
    # ====================================
    path('registro-cliente/', views.client_registration, name='client_registration'),
    path('api/clientes/registro/', views.client_registration_api, name='client_registration_api'),
    path('api/clientes/', views.client_list_api, name='client_list_api'),
    path('api/companias/', views.companies_list_api, name='companies_list_api'),

    # ====================================
    # MÓDULO: REGISTRO DE CONDUCTORES
    # ====================================
    path('registro-conductores/', views.driver_registration, name='driver_registration'),
    path('driver-registration/', views.driver_registration, name='driver_registration'),
    path('api/conductores/registro/', views.driver_registration_api, name='driver_registration_api'),
    path('api/conductores/', views.driver_list_api, name='driver_list_api'),
    path('api/driver-registration/', views.driver_registration_api, name='driver_registration_api'),
    path('api/drivers/', views.driver_list_api, name='driver_list_api'),

    # ====================================
    # MÓDULO: HISTORIAL DE CONDUCTORES
    # ====================================
    path('detalle-conductor/', driver_history_views.driver_history, name='driver_history'),
    path('api/driver/<int:driver_id>/update-status/', driver_history_views.update_driver_status, name='update_driver_status'),
    path('api/driver/<int:driver_id>/generate-report/', driver_history_views.generate_report, name='generate_report'),
    path('api/driver/<int:driver_id>/export-history/', driver_history_views.export_history, name='export_history'),
    path('api/driver/<int:driver_id>/statistics/', driver_history_views.driver_statistics_api, name='driver_statistics_api'),

]
