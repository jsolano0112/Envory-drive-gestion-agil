from django.contrib import admin
from .models import Compania, Cliente, Conductor

# ====================================
# ADMIN: COMPAÑÍA
# ====================================
@admin.register(Compania)
class CompaniaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('nombre', 'nit')
    ordering = ('nombre',)


# ====================================
# ADMIN: CLIENTE
# ====================================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'numero_documento', 'tipo_documento', 'compania', 'activo', 'fecha_registro')
    list_filter = ('tipo_documento', 'compania', 'activo', 'fecha_registro')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'numero_documento')
    readonly_fields = ('fecha_registro',)
    ordering = ('-fecha_registro',)
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': ('segundo_nombre', 'segundo_apellido', 'tipo_documento', 'numero_documento', 'telefono')
        }),
        ('Información Corporativa', {
            'fields': ('compania', 'activo')
        }),
        ('Auditoría', {
            'fields': ('fecha_registro',)
        }),
    )
# ====================================
# ADMIN: CONDUCTOR
# ====================================
@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = (
        'get_nombre_completo',
        'numero_documento',
        'tipo_documento',
        'estado',
        'banco',
        'numero_cuenta',
        'activo',
        'fecha_registro',
    )
    list_filter = ('estado', 'tipo_documento', 'activo', 'fecha_registro', 'banco')
    search_fields = (
        'user__first_name',
        'user__last_name',
        'numero_documento',
        'numero_licencia',
        'banco',
    )
    readonly_fields = ('fecha_registro',)
    ordering = ('-fecha_registro',)

    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': (
                'segundo_nombre',
                'segundo_apellido',
                'tipo_documento',
                'numero_documento',
                'fecha_nacimiento',
                'telefono_principal',
                'telefono_secundario',
                'direccion',
                'ciudad',
            )
        }),
        ('Información de Licencia', {
            'fields': (
                'numero_licencia',
                'licencia_expedicion',
                'licencia_vencimiento',
            )
        }),
        ('Información Bancaria', {
            'fields': (
                'tipo_cuenta',
                'banco',
                'numero_cuenta',
            )
        }),
        ('Estado del Conductor', {
            'fields': ('estado', 'activo')
        }),
        ('Auditoría', {
            'fields': ('fecha_registro',)
        }),
    )
