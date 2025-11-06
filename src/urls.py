from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import driver_history_views

urlpatterns = [
    # Listas
    path('conductores/activos/', views.conductores_activos, name='conductores_activos'),
    path('conductores/inactivos/', views.conductores_inactivos, name='conductores_inactivos'), 
    path('conductores/todos/', views.conductores_todos, name='conductores_todos'),              

    # Detalle y acciones
    path('conductores/<int:id>/', views.detalle_conductor, name='detalle_conductor'),
    path('conductores/<int:id>/activar/', views.activar_conductor, name='activar_conductor'),
    path('conductores/<int:id>/desactivar/', views.desactivar_conductor, name='desactivar_conductor'),
    path('conductores/<int:id>/eliminar/', views.eliminar_conductor, name='eliminar_conductor'),



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
    # Vista principal del historial
    path('detalle-conductor/', driver_history_views.driver_history, name='driver_history'),    
    # API Endpoints para gestión de conductores
    path('api/driver/<int:driver_id>/update-status/', driver_history_views.update_driver_status, name='update_driver_status'),
    path('api/driver/<int:driver_id>/generate-report/', driver_history_views.generate_report, name='generate_report'),
    path('api/driver/<int:driver_id>/export-history/', driver_history_views.export_history, name='export_history'),
    path('api/driver/<int:driver_id>/statistics/', driver_history_views.driver_statistics_api, name='driver_statistics_api'),
    path('api/driver/autocomplete/', driver_history_views.driver_autocomplete_api, name='driver_autocomplete_api'),

    # ====================================
    # MÓDULO: DETALLE DE COMPAÑÍAS
    # ====================================
    # Vista de listado de compañías
    path('companias/', views.companies_list, name='companies_list'),
    # Vista principal del detalle de compañía
    path('detalle-compania/<int:company_id>/', views.company_detail, name='company_detail'),
    
    # API Endpoints para búsqueda y detalle de compañías
    path('api/companias/buscar/', views.company_search_api, name='company_search_api'),
    path('api/companias/<int:company_id>/detalle/', views.company_detail_api, name='company_detail_api'),
    path('api/companias/<int:company_id>/clientes/', views.company_clients_api, name='company_clients_api'),
    
    # API Endpoint para activar/desactivar clientes
    path('api/clientes/<int:client_id>/toggle-status/', views.client_toggle_status_api, name='client_toggle_status_api'),
    
    # API Endpoints para generación de reportes
    path('api/reportes/servicios/', views.generate_services_report_api, name='generate_services_report_api'),
    path('api/reportes/ingresos/', views.generate_income_report_api, name='generate_income_report_api'),
    path('api/reportes/novedades/', views.generate_issues_report_api, name='generate_issues_report_api'),
]
