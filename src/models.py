from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# ====================================
# MODELO: COMPAÑÍA
# ====================================
# Asumido temporalmente - ajustar cuando el Módulo 1 esté disponible
class Compania(models.Model):
    """
    Modelo para las compañías asociadas que tienen acceso a la plataforma.
    Módulo 1 (aprobado) - Este modelo debe existir ya.
    Si hay diferencias, ajustar las referencias en Cliente.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Compañía")
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    estado = models.BooleanField(default=True, verbose_name="Activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'compania'
        verbose_name = 'Compañía'
        verbose_name_plural = 'Compañías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


# ====================================
# MODELO: CLIENTE
# ====================================
class Cliente(models.Model):
    """
    Modelo para los clientes (empleados de compañías asociadas).
    Extiende el modelo User de Django para autenticación.
    """
    
    # Relación con User de Django (maneja: email, password, first_name, last_name)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='cliente',
        verbose_name="Usuario"
    )
    
    # Campos adicionales de nombres
    segundo_nombre = models.CharField(
        max_length=30, 
        blank=True, 
        null=True,
        verbose_name="Segundo Nombre"
    )
    
    segundo_apellido = models.CharField(
        max_length=30, 
        blank=True, 
        null=True,
        verbose_name="Segundo Apellido"
    )
    
    # Tipo de documento
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PAS', 'Pasaporte'),
    ]
    
    tipo_documento = models.CharField(
        max_length=3,
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name="Tipo de Documento"
    )
    
    # Número de documento (único e indexado)
    numero_documento = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^[0-9]+$', 'Solo se permiten números')],
        verbose_name="Número de Documento"
    )
    
    # Teléfono
    telefono_validator = RegexValidator(
        regex=r'^[0-9]{10}$',
        message='El teléfono debe tener 10 dígitos'
    )
    
    telefono = models.CharField(
        max_length=10,
        validators=[telefono_validator],
        verbose_name="Teléfono"
    )
    
    # Compañía asociada (FK)
    compania = models.ForeignKey(
        Compania,
        on_delete=models.CASCADE,
        related_name='clientes',
        verbose_name="Compañía Asociada"
    )
    
    # Campos de auditoría
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['numero_documento']),
            models.Index(fields=['compania']),
        ]
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.compania.nombre}"
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del cliente"""
        nombres = [self.user.first_name]
        if self.segundo_nombre:
            nombres.append(self.segundo_nombre)
        apellidos = [self.user.last_name]
        if self.segundo_apellido:
            apellidos.append(self.segundo_apellido)
        return f"{' '.join(nombres)} {' '.join(apellidos)}"
