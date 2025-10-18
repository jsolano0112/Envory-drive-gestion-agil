from django.contrib import admin
from .models import Compania, Cliente

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
