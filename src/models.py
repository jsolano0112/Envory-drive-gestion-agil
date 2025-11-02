from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
# ====================================
# MODELO: COMPAÑÍA
# ====================================
class Compania(models.Model):
    """
    Modelo para las compañías asociadas que tienen acceso a la plataforma.
    Incluye información detallada para gestión administrativa.
    """
    # Información básica
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Compañía")
    razon_social = models.CharField(max_length=150, blank=True, default='', verbose_name="Razón Social")
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    
    # Información de contacto
    direccion = models.CharField(max_length=200, blank=True, default='', verbose_name="Dirección")
    telefono = models.CharField(
        max_length=10,
        blank=True,
        default='',
        validators=[RegexValidator(r'^[0-9]{10}$', 'El teléfono debe tener 10 dígitos')],
        verbose_name="Teléfono"
    )
    email_corporativo = models.EmailField(blank=True, default='', verbose_name="Email Corporativo")
    persona_contacto = models.CharField(max_length=100, blank=True, default='', verbose_name="Persona de Contacto")
    
    # Información administrativa
    fecha_membresia = models.DateField(null=True, blank=True, verbose_name="Fecha de Membresía")
    
    ESTADO_CUENTA_CHOICES = [
        ('Activa', 'Activa'),
        ('Suspendida', 'Suspendida'),
        ('Morosa', 'Morosa'),
        ('Cancelada', 'Cancelada'),
    ]
    
    estado_cuenta = models.CharField(
        max_length=20,
        choices=ESTADO_CUENTA_CHOICES,
        default='Activa',
        verbose_name="Estado de Cuenta"
    )
    
    # Campo de auditoría
    estado = models.BooleanField(default=True, verbose_name="Activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'compania'
        verbose_name = 'Compañía'
        verbose_name_plural = 'Compañías'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nit']),
            models.Index(fields=['estado_cuenta']),
        ]
    
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
    
    # Campo adicional para detalle de compañía
    cargo = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Cargo/Posición"
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
        ('Pendiente de Verificación', 'Pendiente de Verificación'),
        ('En Corrección', 'En Corrección'),
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Suspendido', 'Suspendido'),
        ('Bloqueado', 'Bloqueado'),
        ('Rechazado', 'Rechazado'),
        ('Dado de Baja', 'Dado de Baja'),
    ]
    
    estado = models.CharField(
        max_length=40,
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
    
# Agregar al final de models.py

# ====================================
# MODELO: VIAJE
# ====================================
class Viaje(models.Model):
    """
    Modelo para los viajes realizados por los conductores.
    """
    
    ESTADO_CHOICES = [
        ('Solicitado', 'Solicitado'),
        ('Aceptado', 'Aceptado'),
        ('En Progreso', 'En Progreso'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
        ('Rechazado', 'Rechazado'),
    ]
    
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
        related_name='viajes',
        verbose_name="Conductor"
    )
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='viajes',
        verbose_name="Cliente"
    )
    
    fecha_solicitud = models.DateTimeField(
        verbose_name="Fecha de Solicitud"
    )
    
    fecha_inicio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Inicio"
    )
    
    fecha_fin = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Fin"
    )
    
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='Solicitado',
        verbose_name="Estado del Viaje"
    )
    
    # Ubicaciones
    origen = models.CharField(
        max_length=100,
        verbose_name="Dirección de Origen"
    )
    
    destino = models.CharField(
        max_length=100,
        verbose_name="Dirección de Destino"
    )
    
    # Información del viaje
    distancia_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Distancia (km)"
    )
    
    tiempo_estimado = models.DurationField(
        null=True,
        blank=True,
        verbose_name="Tiempo Estimado"
    )
    
    tiempo_real = models.DurationField(
        null=True,
        blank=True,
        verbose_name="Tiempo Real"
    )
    
    # Calificación y comentarios
    calificacion_cliente = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación del Cliente"
    )
    
    comentario_cliente = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comentario del Cliente"
    )
    
    calificacion_conductor = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación del Conductor"
    )
    
    comentario_conductor = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comentario del Conductor"
    )
    
    # Costos
    valor_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Base"
    )
    
    valor_adicional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Valor Adicional"
    )
    
    descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Descuento"
    )
    
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Total"
    )
    
    # Método de pago
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
        ('Transferencia', 'Transferencia Bancaria'),
        ('App', 'Pago en App'),
    ]
    
    metodo_pago = models.CharField(
        max_length=15,
        choices=METODO_PAGO_CHOICES,
        default='Efectivo',
        verbose_name="Método de Pago"
    )
    
    # Información adicional
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas Adicionales"
    )
    
    class Meta:
        db_table = 'viaje'
        verbose_name = 'Viaje'
        verbose_name_plural = 'Viajes'
        ordering = ['-fecha_solicitud']
        indexes = [
            models.Index(fields=['conductor', '-fecha_solicitud']),
            models.Index(fields=['cliente', '-fecha_solicitud']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_solicitud']),
        ]
    
    def __str__(self):
        return f"Viaje {self.id} - {self.conductor.get_nombre_completo()} → {self.origen[:30]}"
    
    def get_duracion_formateada(self):
        """Retorna la duración en formato legible"""
        if self.tiempo_real:
            total_seconds = int(self.tiempo_real.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "N/A"


# ====================================
# MODELO: HISTORIAL DE ESTADOS
# ====================================
class HistorialEstadoConductor(models.Model):
    """
    Modelo para mantener el historial de cambios de estado de los conductores.
    """
    
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
        related_name='historial_estados',
        verbose_name="Conductor"
    )
    
    estado_anterior = models.CharField(
        max_length=40,
        choices=Conductor.ESTADO_CHOICES,
        verbose_name="Estado Anterior"
    )
    
    estado_nuevo = models.CharField(
        max_length=40,
        choices=Conductor.ESTADO_CHOICES,
        verbose_name="Estado Nuevo"
    )
    
    fecha_cambio = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha del Cambio"
    )
    
    MOTIVO_CHOICES = [
        ('Registro', 'Registro inicial'),
        ('Verificacion', 'Verificación de documentos'),
        ('Correccion', 'Solicitud de corrección'),
        ('Aprobacion', 'Aprobación de documentos'),
        ('Activacion', 'Activación manual'),
        ('Inactivacion', 'Inactivación voluntaria'),
        ('Suspension', 'Suspensión por incumplimiento'),
        ('Bloqueo', 'Bloqueo por infracciones graves'),
        ('Rechazo', 'Rechazo por no cumplir requisitos'),
        ('Baja', 'Dado de baja'),
        ('Reactivacion', 'Reactivación por cumplimiento'),
        ('Licencia', 'Licencia vencida'),
        ('Queja', 'Queja de cliente'),
        ('Pago', 'Pago pendiente'),
        ('Otro', 'Otro motivo'),
    ]
    
    motivo = models.CharField(
        max_length=20,
        choices=MOTIVO_CHOICES,
        default='Manual',
        verbose_name="Motivo del Cambio"
    )
    
    descripcion_motivo = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción del Motivo"
    )
    
    usuario_modificador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cambios_estado_conductores',
        verbose_name="Usuario que realizó el cambio"
    )
    
    # Información adicional
    notas_internas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas Internas"
    )
    
    # Campos automáticos
    ip_modificador = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP del modificador"
    )
    
    user_agent = models.TextField(
        blank=True,
        null=True,
        verbose_name="User Agent"
    )
    
    class Meta:
        db_table = 'historial_estado_conductor'
        verbose_name = 'Cambio de Estado del Conductor'
        verbose_name_plural = 'Historial de Estados de Conductores'
        ordering = ['-fecha_cambio']
        indexes = [
            models.Index(fields=['conductor', '-fecha_cambio']),
            models.Index(fields=['fecha_cambio']),
            models.Index(fields=['motivo']),
        ]
    
    def __str__(self):
        return f"{self.conductor.get_nombre_completo()} - {self.estado_anterior} → {self.estado_nuevo}"
    
    def get_titulo_cambio(self):
        """Retorna un título descriptivo del cambio"""
        transiciones = {
            ('Pendiente', 'Aprobado'): 'Conductor Aprobado',
            ('Pendiente', 'Rechazado'): 'Conductor Rechazado',
            ('Aprobado', 'Suspendido'): 'Conductor Suspendido',
            ('Suspendido', 'Aprobado'): 'Conductor Reactivado',
            ('Aprobado', 'Activo'): 'Conductor Activado',
            ('Activo', 'Inactivo'): 'Conductor Desactivado',
        }
        return transiciones.get((self.estado_anterior, self.estado_nuevo), 
                               f'Cambio de Estado: {self.estado_anterior} → {self.estado_nuevo}')


# ====================================
# MODELO: NOVEDAD
# ====================================
class Novedad(models.Model):
    """
    Modelo para registrar novedades relacionadas con viajes, conductores o clientes.
    """
    
    TIPO_NOVEDAD_CHOICES = [
        ('Accidente', 'Accidente'),
        ('Retraso', 'Retraso'),
        ('Cancelación', 'Cancelación'),
        ('Queja Cliente', 'Queja del Cliente'),
        ('Queja Conductor', 'Queja del Conductor'),
        ('Vehículo Averiado', 'Vehículo Averiado'),
        ('Cambio de Ruta', 'Cambio de Ruta'),
        ('Incidente', 'Incidente'),
        ('Otro', 'Otro'),
    ]
    
    ESTADO_NOVEDAD_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Revisión', 'En Revisión'),
        ('Resuelta', 'Resuelta'),
        ('Cerrada', 'Cerrada'),
        ('Escalada', 'Escalada'),
    ]
    
    # Relaciones
    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE,
        related_name='novedades',
        null=True,
        blank=True,
        verbose_name="Viaje Asociado"
    )
    
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
        related_name='novedades',
        null=True,
        blank=True,
        verbose_name="Conductor Involucrado"
    )
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='novedades',
        null=True,
        blank=True,
        verbose_name="Cliente Involucrado"
    )
    
    compania = models.ForeignKey(
        Compania,
        on_delete=models.CASCADE,
        related_name='novedades',
        null=True,
        blank=True,
        verbose_name="Compañía Asociada"
    )
    
    # Información de la novedad
    tipo_novedad = models.CharField(
        max_length=30,
        choices=TIPO_NOVEDAD_CHOICES,
        verbose_name="Tipo de Novedad"
    )
    
    descripcion = models.TextField(verbose_name="Descripción")
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_NOVEDAD_CHOICES,
        default='Pendiente',
        verbose_name="Estado"
    )
    
    # Auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='novedades_creadas',
        verbose_name="Creado Por"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    fecha_resolucion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Resolución"
    )
    
    resolucion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Resolución"
    )
    
    resuelto_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='novedades_resueltas',
        verbose_name="Resuelto Por"
    )
    
    # Prioridad
    PRIORIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
        ('Crítica', 'Crítica'),
    ]
    
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='Media',
        verbose_name="Prioridad"
    )
    
    class Meta:
        db_table = 'novedad'
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['tipo_novedad']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_creacion']),
            models.Index(fields=['compania', '-fecha_creacion']),
        ]
    
    def __str__(self):
        return f"{self.tipo_novedad} - {self.estado} ({self.fecha_creacion.strftime('%Y-%m-%d')})"