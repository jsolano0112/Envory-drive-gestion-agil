from django.urls import path
from django.contrib.auth import views as auth_views
from .views import views
from .views import driver_history_views

urlpatterns = [
    
    # Listas: ahora muestran todos los conductores
    path('conductores/activos/', views.conductores_todos, name='conductores_activos'),
    path('conductores/inactivos/', views.conductores_todos, name='conductores_inactivos'),
    path('conductores/todos/', views.conductores_todos, name='conductores_todos'),

    # Detalle (si lo necesitas)
    path('conductores/<int:id>/', views.detalle_conductor, name='detalle_conductor'),

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
    path('api/conductores/', views.driver_list_api, name='driver_list_api'),
    path('api/conductores/registro/', views.driver_registration_api, name='driver_registration_api'),

    # ====================================
    # MÓDULO: HISTORIAL DE CONDUCTORES
    # ====================================
    path('detalle-conductor/', driver_history_views.driver_history, name='driver_history'),
    path('api/conductores/<int:driver_id>/update-status/', driver_history_views.update_driver_status, name='update_driver_status'),
    path('api/conductores/<int:driver_id>/generate-report/', driver_history_views.generate_report, name='generate_report'),
    path('api/conductores/<int:driver_id>/export-history/', driver_history_views.export_history, name='export_history'),
    path('api/conductores/<int:driver_id>/statistics/', driver_history_views.driver_statistics_api, name='driver_statistics_api'),
    path('api/conductores/autocompletado/', driver_history_views.driver_autocomplete_api, name='driver_autocomplete_api'),

    # ====================================
    # MÓDULO: DETALLE DE COMPAÑÍAS
    # ====================================
    path('companias/', views.companies_list, name='companies_list'),
    path('detalle-compania/<int:company_id>/', views.company_detail, name='company_detail'),
    path('api/companias/buscar/', views.company_search_api, name='company_search_api'),
    path('api/companias/<int:company_id>/detalle/', views.company_detail_api, name='company_detail_api'),
    path('api/companias/<int:company_id>/clientes/', views.company_clients_api, name='company_clients_api'),
    path('api/clientes/<int:client_id>/toggle-status/', views.client_toggle_status_api, name='client_toggle_status_api'),
    path('api/reportes/servicios/', views.generate_services_report_api, name='generate_services_report_api'),
    path('api/reportes/ingresos/', views.generate_income_report_api, name='generate_income_report_api'),
    path('api/reportes/novedades/', views.generate_issues_report_api, name='generate_issues_report_api'),
]
