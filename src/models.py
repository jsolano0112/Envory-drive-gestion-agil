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


# ====================================
# MODELO: CONDUCTOR
# ====================================
class Conductor(models.Model):
    """
    Modelo para los conductores de la plataforma.
    Extiende el modelo User de Django para autenticación.
    """
    
    # Relación con User de Django (maneja: email, password, first_name, last_name)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='conductor',
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
    
    # Fecha de nacimiento
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de Nacimiento"
    )
    
    # Teléfonos
    telefono_principal = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^[0-9]{10}$', 'El teléfono debe tener 10 dígitos')],
        verbose_name="Teléfono Principal"
    )
    
    telefono_secundario = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^[0-9]{10}$', 'El teléfono debe tener 10 dígitos')],
        verbose_name="Teléfono Secundario"
    )
    
    # Dirección
    direccion = models.CharField(
        max_length=60,
        verbose_name="Dirección de Residencia"
    )
    
    ciudad = models.CharField(
        max_length=30,
        verbose_name="Ciudad"
    )
    
    # Información de licencia
    numero_licencia = models.CharField(
        max_length=20,
        verbose_name="Número de Licencia"
    )
    
    licencia_expedicion = models.DateField(
        verbose_name="Fecha de Expedición de Licencia"
    )
    
    licencia_vencimiento = models.DateField(
        verbose_name="Fecha de Vencimiento de Licencia"
    )
    
    # Información bancaria
    TIPO_CUENTA_CHOICES = [
        ('Ahorros', 'Ahorros'),
        ('Corriente', 'Corriente'),
    ]
    
    tipo_cuenta = models.CharField(
        max_length=10,
        choices=TIPO_CUENTA_CHOICES,
        verbose_name="Tipo de Cuenta"
    )
    
    banco = models.CharField(
        max_length=50,
        verbose_name="Banco"
    )
    
    numero_cuenta = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^[0-9]+$', 'Solo se permiten números')],
        verbose_name="Número de Cuenta"
    )
    
    # Estados del conductor
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente de Verificación'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
        ('Suspendido', 'Suspendido'),
    ]
    
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='Pendiente',
        verbose_name="Estado"
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
        db_table = 'conductor'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['numero_documento']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.numero_documento}"
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del conductor"""
        nombres = [self.user.first_name]
        if self.segundo_nombre:
            nombres.append(self.segundo_nombre)
        apellidos = [self.user.last_name]
        if self.segundo_apellido:
            apellidos.append(self.segundo_apellido)
        return f"{' '.join(nombres)} {' '.join(apellidos)}"
    
    def get_edad(self):
        """Calcula la edad del conductor"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))


# ====================================
# MODELO: VEHÍCULO
# ====================================
class Vehiculo(models.Model):
    """
    Modelo para los vehículos de los conductores.
    """
    
    conductor = models.OneToOneField(
        Conductor,
        on_delete=models.CASCADE,
        related_name='vehiculo',
        verbose_name="Conductor"
    )
    
    # Datos básicos del vehículo
    placa = models.CharField(
        max_length=6,
        unique=True,
        verbose_name="Placa del Vehículo"
    )
    
    marca = models.CharField(
        max_length=30,
        verbose_name="Marca del Vehículo"
    )
    
    modelo = models.CharField(
        max_length=30,
        verbose_name="Modelo del Vehículo"
    )
    
    anio = models.PositiveIntegerField(
        verbose_name="Año del Vehículo"
    )
    
    color = models.CharField(
        max_length=20,
        verbose_name="Color del Vehículo"
    )
    
    tipo_vehiculo = models.CharField(
        max_length=20,
        verbose_name="Tipo de Vehículo"
    )
    
    num_pasajeros = models.PositiveIntegerField(
        verbose_name="Número de Pasajeros"
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
        db_table = 'vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['placa']),
            models.Index(fields=['conductor']),
        ]
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"


# ====================================
# MODELO: DOCUMENTO CONDUCTOR
# ====================================
class DocumentoConductor(models.Model):
    """
    Modelo para almacenar los documentos subidos por los conductores.
    """
    
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name="Conductor"
    )
    
    TIPO_DOCUMENTO_CHOICES = [
        ('documento_frontal', 'Documento de Identidad Frontal'),
        ('documento_reverso', 'Documento de Identidad Reverso'),
        ('tarjeta_propiedad', 'Tarjeta de Propiedad'),
        ('certificado_reconocimiento', 'Certificado de Reconocimiento'),
        ('foto_licencia', 'Foto de Licencia'),
        ('documento_soat', 'Documento SOAT'),
        ('antecedentes_judiciales', 'Antecedentes Judiciales'),
        ('foto_vehiculo_frontal', 'Foto Vehículo Frontal'),
        ('foto_vehiculo_lateral', 'Foto Vehículo Lateral'),
        ('foto_vehiculo_interior', 'Foto Vehículo Interior'),
        ('certificado_tecnomecanica', 'Certificado de Tecnomecánica'),
    ]
    
    tipo_documento = models.CharField(
        max_length=30,
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name="Tipo de Documento"
    )
    
    archivo = models.FileField(
        upload_to='documentos_conductores/%Y/%m/%d/',
        verbose_name="Archivo"
    )
    
    nombre_original = models.CharField(
        max_length=255,
        verbose_name="Nombre Original del Archivo"
    )
    
    tamaño_archivo = models.PositiveIntegerField(
        verbose_name="Tamaño del Archivo (bytes)"
    )
    
    # Campos de auditoría
    fecha_subida = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Subida"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        db_table = 'documento_conductor'
        verbose_name = 'Documento de Conductor'
        verbose_name_plural = 'Documentos de Conductores'
        ordering = ['-fecha_subida']
        indexes = [
            models.Index(fields=['conductor']),
            models.Index(fields=['tipo_documento']),
        ]
    
    def __str__(self):
        return f"{self.conductor.get_nombre_completo()} - {self.get_tipo_documento_display()}"