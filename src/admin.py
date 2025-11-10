from django.contrib import admin
from .models.models import Compania, Cliente, Conductor, Novedad

# ====================================
# ADMIN: COMPAÑÍA
# ====================================
@admin.register(Compania)
class CompaniaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'razon_social', 'telefono', 'estado_cuenta', 'estado', 'fecha_membresia')
    list_filter = ('estado', 'estado_cuenta', 'fecha_creacion')
    search_fields = ('nombre', 'nit', 'razon_social', 'persona_contacto')
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'razon_social', 'nit')
        }),
        ('Información de Contacto', {
            'fields': ('direccion', 'telefono', 'email_corporativo', 'persona_contacto')
        }),
        ('Información Administrativa', {
            'fields': ('fecha_membresia', 'estado_cuenta', 'estado')
        }),
    )


# ====================================
# ADMIN: CLIENTE
# ====================================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'numero_documento', 'tipo_documento', 'cargo', 'compania', 'activo', 'fecha_registro')
    list_filter = ('tipo_documento', 'compania', 'activo', 'fecha_registro')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'numero_documento', 'cargo')
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
            'fields': ('compania', 'cargo', 'activo')
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


# ====================================
# ADMIN: NOVEDAD
# ====================================
@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_novedad', 'estado', 'compania', 'creado_por', 'fecha_creacion', 'prioridad')
    list_filter = ('tipo_novedad', 'estado', 'prioridad', 'fecha_creacion', 'compania')
    search_fields = ('descripcion', 'tipo_novedad', 'compania__nombre')
    readonly_fields = ('fecha_creacion', 'creado_por', 'resuelto_por', 'fecha_resolucion')
    ordering = ('-fecha_creacion',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('tipo_novedad', 'estado', 'prioridad', 'descripcion')
        }),
        ('Relaciones', {
            'fields': ('viaje', 'conductor', 'cliente', 'compania')
        }),
        ('Resolución', {
            'fields': ('resolucion', 'fecha_resolucion', 'resuelto_por')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion')
        }),
    )
