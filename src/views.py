from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction, IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json
import re

from .models import Cliente, Compania, Conductor, Vehiculo, DocumentoConductor

# ====================================
# VISTAS EXISTENTES
# ====================================
@login_required
def index(request):
    return render(request, 'index.html')

def inicio(request):
    return HttpResponse("¡Hola! Esta es la primera página web con Django.")

def driver_registration(request):
    return render(request, 'driver_registration.html')

def login(request):
    return render(request, 'login.html')


# ====================================
# MÓDULO: REGISTRO DE CLIENTES
# ====================================

def client_registration(request):
    """
    Vista que renderiza el formulario de registro de clientes.
    GET: Muestra el formulario
    """
    return render(request, 'client_registration.html')


@csrf_exempt
@require_http_methods(["POST"])
def client_registration_api(request):
    """
    Endpoint POST para registrar nuevos clientes.
    Valida datos, verifica duplicados y crea el usuario + perfil de cliente.
    
    Respuesta JSON:
    - success: true/false
    - message: mensaje descriptivo
    - data: información adicional (opcional)
    """
    try:
        # Parsear datos JSON del request
        data = json.loads(request.body)
        
        # ===================================
        # VALIDACIÓN DE CAMPOS OBLIGATORIOS
        # ===================================
        required_fields = [
            'primer_nombre', 'primer_apellido', 'tipo_documento',
            'numero_documento', 'correo', 'telefono', 'compania_id', 'password'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'message': 'Error: faltan campos obligatorios',
                'missing_fields': missing_fields
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE FORMATO DE NOMBRES
        # ===================================
        # Solo letras y espacios (sin números ni símbolos)
        name_pattern = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')
        
        if not name_pattern.match(data['primer_nombre']):
            return JsonResponse({
                'success': False,
                'message': 'El primer nombre no debe contener números ni símbolos'
            }, status=400)
        
        if not name_pattern.match(data['primer_apellido']):
            return JsonResponse({
                'success': False,
                'message': 'El primer apellido no debe contener números ni símbolos'
            }, status=400)
        
        if data.get('segundo_nombre') and not name_pattern.match(data['segundo_nombre']):
            return JsonResponse({
                'success': False,
                'message': 'El segundo nombre no debe contener números ni símbolos'
            }, status=400)
        
        if data.get('segundo_apellido') and not name_pattern.match(data['segundo_apellido']):
            return JsonResponse({
                'success': False,
                'message': 'El segundo apellido no debe contener números ni símbolos'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE EMAIL
        # ===================================
        email = data['correo'].lower().strip()
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'message': 'Verificar correo'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE CONTRASEÑA
        # ===================================
        password = data['password']
        confirm_password = data.get('confirm_password', '')
        
        # Verificar coincidencia
        if password != confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'Las contraseñas no coinciden'
            }, status=400)
        
        # Validar requisitos: mínimo 8 caracteres, mayúscula, minúscula, número
        if len(password) < 8:
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe tener mínimo 8 caracteres'
            }, status=400)
        
        if not re.search(r'[A-Z]', password):
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe contener al menos una mayúscula'
            }, status=400)
        
        if not re.search(r'[a-z]', password):
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe contener al menos una minúscula'
            }, status=400)
        
        if not re.search(r'\d', password):
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe contener al menos un número'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE NÚMERO DE DOCUMENTO
        # ===================================
        numero_documento = data['numero_documento'].strip()
        if not numero_documento.isdigit():
            return JsonResponse({
                'success': False,
                'message': 'El número de documento solo debe contener números'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE TELÉFONO
        # ===================================
        telefono = data['telefono'].strip()
        if not re.match(r'^[0-9]{10}$', telefono):
            return JsonResponse({
                'success': False,
                'message': 'El teléfono debe tener 10 dígitos'
            }, status=400)
        
        # ===================================
        # VERIFICAR USUARIO NO EXISTENTE
        # ===================================
        
        # Verificar por email
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'El usuario se encuentra registrado'
            }, status=409)
        
        # Verificar por número de documento
        if Cliente.objects.filter(numero_documento=numero_documento).exists():
            return JsonResponse({
                'success': False,
                'message': 'El usuario se encuentra registrado'
            }, status=409)
        
        # ===================================
        # VERIFICAR QUE LA COMPAÑÍA EXISTE
        # ===================================
        try:
            compania = Compania.objects.get(id=data['compania_id'], estado=True)
        except Compania.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'La compañía seleccionada no es válida'
            }, status=400)
        
        # ===================================
        # CREAR USUARIO Y CLIENTE
        # ===================================
        with transaction.atomic():
            # Crear usuario de Django
            user = User.objects.create_user(
                username=email,  # Usamos el email como username
                email=email,
                password=password,
                first_name=data['primer_nombre'].strip(),
                last_name=data['primer_apellido'].strip()
            )
            
            # Crear perfil de cliente
            cliente = Cliente.objects.create(
                user=user,
                segundo_nombre=data.get('segundo_nombre', '').strip(),
                segundo_apellido=data.get('segundo_apellido', '').strip(),
                tipo_documento=data['tipo_documento'],
                numero_documento=numero_documento,
                telefono=telefono,
                compania=compania
            )
        
        return JsonResponse({
            'success': True,
            'message': 'El registro fue exitoso',
            'data': {
                'cliente_id': cliente.id,
                'nombre_completo': cliente.get_nombre_completo(),
                'email': email
            }
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error en el formato de los datos'
        }, status=400)
    
    except IntegrityError as e:
        return JsonResponse({
            'success': False,
            'message': 'Error de integridad en la base de datos'
        }, status=500)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def client_list_api(request):
    """
    Endpoint GET para consultar clientes.
    Permite filtrar por: email, numero_documento, compania_id
    
    Query params:
    - email: filtrar por email
    - numero_documento: filtrar por número de documento
    - compania_id: filtrar por compañía
    - activo: filtrar por estado (true/false)
    
    Requiere permisos de administrador (validación básica).
    """
    try:
        # TODO: Implementar validación de permisos de administrador
        # Por ahora permitimos la consulta
        
        # Obtener parámetros de filtro
        email = request.GET.get('email')
        numero_documento = request.GET.get('numero_documento')
        compania_id = request.GET.get('compania_id')
        activo = request.GET.get('activo')
        
        # Iniciar queryset
        clientes = Cliente.objects.select_related('user', 'compania').all()
        
        # Aplicar filtros
        if email:
            clientes = clientes.filter(user__email__icontains=email)
        
        if numero_documento:
            clientes = clientes.filter(numero_documento=numero_documento)
        
        if compania_id:
            clientes = clientes.filter(compania_id=compania_id)
        
        if activo is not None:
            activo_bool = activo.lower() == 'true'
            clientes = clientes.filter(activo=activo_bool)
        
        # Serializar datos (sin incluir contraseñas)
        clientes_data = []
        for cliente in clientes:
            clientes_data.append({
                'id': cliente.id,
                'nombre_completo': cliente.get_nombre_completo(),
                'primer_nombre': cliente.user.first_name,
                'segundo_nombre': cliente.segundo_nombre,
                'primer_apellido': cliente.user.last_name,
                'segundo_apellido': cliente.segundo_apellido,
                'tipo_documento': cliente.tipo_documento,
                'numero_documento': cliente.numero_documento,
                'email': cliente.user.email,
                'telefono': cliente.telefono,
                'compania': {
                    'id': cliente.compania.id,
                    'nombre': cliente.compania.nombre
                },
                'activo': cliente.activo,
                'fecha_registro': cliente.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'success': True,
            'count': len(clientes_data),
            'data': clientes_data
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al consultar clientes: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def companies_list_api(request):
    """
    Endpoint GET para obtener lista de compañías activas.
    Usado para popular el select del formulario de registro.
    """
    try:
        companias = Compania.objects.filter(estado=True).order_by('nombre')
        
        companias_data = [
            {
                'id': c.id,
                'nombre': c.nombre
            }
            for c in companias
        ]
        
        return JsonResponse({
            'success': True,
            'data': companias_data
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al consultar compañías: {str(e)}'
        }, status=500)


# ====================================
# MÓDULO: REGISTRO DE CONDUCTORES
# ====================================

@csrf_exempt
@require_http_methods(["POST"])
def driver_registration_api(request):
    """
    Endpoint POST para registrar nuevos conductores.
    Valida datos, verifica duplicados y crea el usuario + perfil de conductor + vehículo + documentos.
    
    Respuesta JSON:
    - success: true/false
    - message: mensaje descriptivo
    - data: información adicional (opcional)
    """
    try:
        # Parsear datos del formulario (multipart/form-data)
        data = request.POST
        files = request.FILES
        
        # ===================================
        # VALIDACIÓN DE CAMPOS OBLIGATORIOS
        # ===================================
        required_fields = [
            'primer_nombre', 'primer_apellido', 'tipo_documento',
            'numero_documento', 'fecha_nacimiento', 'correo', 
            'telefono_principal', 'direccion', 'ciudad', 'password',
            'numero_licencia', 'licencia_expedicion', 'licencia_vencimiento',
            'tipo_cuenta', 'banco', 'numero_cuenta', 'confirmar_numero_cuenta',
            'placa', 'marca', 'modelo', 'anio', 'color', 'tipo_vehiculo', 'num_pasajeros'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'message': 'Error: faltan campos obligatorios',
                'missing_fields': missing_fields
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE FORMATO DE NOMBRES
        # ===================================
        name_pattern = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')
        
        if not name_pattern.match(data['primer_nombre']):
            return JsonResponse({
                'success': False,
                'message': 'El primer nombre no debe contener números ni símbolos'
            }, status=400)
        
        if not name_pattern.match(data['primer_apellido']):
            return JsonResponse({
                'success': False,
                'message': 'El primer apellido no debe contener números ni símbolos'
            }, status=400)
        
        if data.get('segundo_nombre') and not name_pattern.match(data['segundo_nombre']):
            return JsonResponse({
                'success': False,
                'message': 'El segundo nombre no debe contener números ni símbolos'
            }, status=400)
        
        if data.get('segundo_apellido') and not name_pattern.match(data['segundo_apellido']):
            return JsonResponse({
                'success': False,
                'message': 'El segundo apellido no debe contener números ni símbolos'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE EMAIL
        # ===================================
        email = data['correo'].lower().strip()
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'message': 'Verificar correo'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE CONTRASEÑA
        # ===================================
        password = data['password']
        confirm_password = data.get('confirm_password', '')
        
        if password != confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'Las contraseñas no coinciden'
            }, status=400)
        
        # Validar requisitos de contraseña
        if len(password) < 8:
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe tener mínimo 8 caracteres'
            }, status=400)
        
        if not re.search(r'[A-Z]', password):
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe contener al menos una mayúscula'
            }, status=400)
        
        if not re.search(r'[a-z]', password):
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe contener al menos una minúscula'
            }, status=400)
        
        if not re.search(r'\d', password):
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe contener al menos un número'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE FECHA DE NACIMIENTO (EDAD MÍNIMA 21 AÑOS)
        # ===================================
        from datetime import date, datetime
        fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
        today = date.today()
        age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        if age < 21:
            return JsonResponse({
                'success': False,
                'message': 'El conductor debe ser mayor de 21 años'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE NÚMERO DE DOCUMENTO
        # ===================================
        numero_documento = data['numero_documento'].strip()
        if not numero_documento.isdigit():
            return JsonResponse({
                'success': False,
                'message': 'El número de documento solo debe contener números'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE TELÉFONOS
        # ===================================
        telefono_principal = data['telefono_principal'].strip()
        if not re.match(r'^[0-9]{10}$', telefono_principal):
            return JsonResponse({
                'success': False,
                'message': 'El teléfono principal debe tener 10 dígitos'
            }, status=400)
        
        telefono_secundario = data.get('telefono_secundario', '').strip()
        if telefono_secundario and not re.match(r'^[0-9]{10}$', telefono_secundario):
            return JsonResponse({
                'success': False,
                'message': 'El teléfono secundario debe tener 10 dígitos'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE NÚMEROS DE CUENTA
        # ===================================
        numero_cuenta = data['numero_cuenta'].strip()
        confirmar_numero_cuenta = data['confirmar_numero_cuenta'].strip()
        
        if numero_cuenta != confirmar_numero_cuenta:
            return JsonResponse({
                'success': False,
                'message': 'Los números de cuenta no coinciden'
            }, status=400)
        
        if not numero_cuenta.isdigit():
            return JsonResponse({
                'success': False,
                'message': 'El número de cuenta solo debe contener números'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE PLACA
        # ===================================
        placa = data['placa'].strip().upper()
        if not re.match(r'^[A-Z]{3}[0-9]{3}$', placa):
            return JsonResponse({
                'success': False,
                'message': 'La placa debe tener formato ABC123'
            }, status=400)
        
        # ===================================
        # VERIFICAR USUARIO NO EXISTENTE
        # ===================================
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'El usuario se encuentra registrado'
            }, status=409)
        
        if Conductor.objects.filter(numero_documento=numero_documento).exists():
            return JsonResponse({
                'success': False,
                'message': 'El conductor se encuentra registrado'
            }, status=409)
        
        if Vehiculo.objects.filter(placa=placa).exists():
            return JsonResponse({
                'success': False,
                'message': 'La placa del vehículo ya está registrada'
            }, status=409)
        
        # ===================================
        # VALIDACIÓN DE FECHAS DE LICENCIA
        # ===================================
        licencia_expedicion = datetime.strptime(data['licencia_expedicion'], '%Y-%m-%d').date()
        licencia_vencimiento = datetime.strptime(data['licencia_vencimiento'], '%Y-%m-%d').date()
        
        if licencia_vencimiento <= licencia_expedicion:
            return JsonResponse({
                'success': False,
                'message': 'La fecha de vencimiento debe ser posterior a la fecha de expedición'
            }, status=400)
        
        if licencia_vencimiento <= today:
            return JsonResponse({
                'success': False,
                'message': 'La licencia de conducción está vencida'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE AÑO DEL VEHÍCULO
        # ===================================
        anio_vehiculo = int(data['anio'])
        if anio_vehiculo < 2015 or anio_vehiculo > today.year:
            return JsonResponse({
                'success': False,
                'message': 'El año del vehículo debe estar entre 2015 y el año actual'
            }, status=400)
        
        # ===================================
        # VALIDACIÓN DE ARCHIVOS OBLIGATORIOS
        # ===================================
        required_files = [
            'documento_frontal', 'tarjeta_propiedad', 'certificado_reconocimiento',
            'foto_licencia', 'documento_soat', 'antecedentes_judiciales',
            'foto_vehiculo_frontal', 'foto_vehiculo_lateral', 'foto_vehiculo_interior',
            'certificado_tecnomecanica'
        ]
        
        missing_files = [file for file in required_files if file not in files]
        if missing_files:
            return JsonResponse({
                'success': False,
                'message': 'Faltan archivos obligatorios',
                'missing_files': missing_files
            }, status=400)
        
        # ===================================
        # CREAR USUARIO, CONDUCTOR, VEHÍCULO Y DOCUMENTOS
        # ===================================
        with transaction.atomic():
            # Crear usuario de Django
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=data['primer_nombre'].strip(),
                last_name=data['primer_apellido'].strip()
            )
            
            # Crear perfil de conductor
            conductor = Conductor.objects.create(
                user=user,
                segundo_nombre=data.get('segundo_nombre', '').strip() or None,
                segundo_apellido=data.get('segundo_apellido', '').strip() or None,
                tipo_documento=data['tipo_documento'],
                numero_documento=numero_documento,
                fecha_nacimiento=fecha_nacimiento,
                telefono_principal=telefono_principal,
                telefono_secundario=telefono_secundario or None,
                direccion=data['direccion'].strip(),
                ciudad=data['ciudad'],
                numero_licencia=data['numero_licencia'].strip(),
                licencia_expedicion=licencia_expedicion,
                licencia_vencimiento=licencia_vencimiento,
                tipo_cuenta=data['tipo_cuenta'],
                banco=data['banco'],
                numero_cuenta=numero_cuenta
            )
            
            # Crear vehículo
            vehiculo = Vehiculo.objects.create(
                conductor=conductor,
                placa=placa,
                marca=data['marca'].strip().upper(),
                modelo=data['modelo'].strip(),
                anio=anio_vehiculo,
                color=data['color'].strip(),
                tipo_vehiculo=data['tipo_vehiculo'].strip(),
                num_pasajeros=int(data['num_pasajeros'])
            )
            
            # Crear documentos
            documento_types = {
                'documento_frontal': 'documento_frontal',
                'documento_reverso': 'documento_reverso',
                'tarjeta_propiedad': 'tarjeta_propiedad',
                'certificado_reconocimiento': 'certificado_reconocimiento',
                'foto_licencia': 'foto_licencia',
                'documento_soat': 'documento_soat',
                'antecedentes_judiciales': 'antecedentes_judiciales',
                'foto_vehiculo_frontal': 'foto_vehiculo_frontal',
                'foto_vehiculo_lateral': 'foto_vehiculo_lateral',
                'foto_vehiculo_interior': 'foto_vehiculo_interior',
                'certificado_tecnomecanica': 'certificado_tecnomecanica'
            }
            
            for file_field, tipo_doc in documento_types.items():
                if file_field in files:
                    file = files[file_field]
                    DocumentoConductor.objects.create(
                        conductor=conductor,
                        tipo_documento=tipo_doc,
                        archivo=file,
                        nombre_original=file.name,
                        tamaño_archivo=file.size
                    )
        
        return JsonResponse({
            'success': True,
            'message': 'El registro del conductor fue exitoso. Estado: Pendiente de Verificación',
            'data': {
                'conductor_id': conductor.id,
                'nombre_completo': conductor.get_nombre_completo(),
                'email': email,
                'estado': conductor.estado,
                'vehiculo_placa': vehiculo.placa
            }
        }, status=201)
    
    except IntegrityError as e:
        return JsonResponse({
            'success': False,
            'message': 'Error de integridad en la base de datos'
        }, status=500)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def driver_list_api(request):
    """
    Endpoint GET para consultar conductores.
    Permite filtrar por: email, numero_documento, estado, placa
    """
    try:
        # Obtener parámetros de filtro
        email = request.GET.get('email')
        numero_documento = request.GET.get('numero_documento')
        estado = request.GET.get('estado')
        placa = request.GET.get('placa')
        activo = request.GET.get('activo')
        
        # Iniciar queryset
        conductores = Conductor.objects.select_related('user', 'vehiculo').all()
        
        # Aplicar filtros
        if email:
            conductores = conductores.filter(user__email__icontains=email)
        
        if numero_documento:
            conductores = conductores.filter(numero_documento=numero_documento)
        
        if estado:
            conductores = conductores.filter(estado=estado)
        
        if placa:
            conductores = conductores.filter(vehiculo__placa__icontains=placa)
        
        if activo is not None:
            activo_bool = activo.lower() == 'true'
            conductores = conductores.filter(activo=activo_bool)
        
        # Serializar datos
        conductores_data = []
        for conductor in conductores:
            vehiculo_data = None
            if hasattr(conductor, 'vehiculo'):
                vehiculo_data = {
                    'placa': conductor.vehiculo.placa,
                    'marca': conductor.vehiculo.marca,
                    'modelo': conductor.vehiculo.modelo,
                    'anio': conductor.vehiculo.anio,
                    'color': conductor.vehiculo.color,
                    'tipo_vehiculo': conductor.vehiculo.tipo_vehiculo,
                    'num_pasajeros': conductor.vehiculo.num_pasajeros
                }
            
            conductores_data.append({
                'id': conductor.id,
                'nombre_completo': conductor.get_nombre_completo(),
                'primer_nombre': conductor.user.first_name,
                'segundo_nombre': conductor.segundo_nombre,
                'primer_apellido': conductor.user.last_name,
                'segundo_apellido': conductor.segundo_apellido,
                'tipo_documento': conductor.tipo_documento,
                'numero_documento': conductor.numero_documento,
                'fecha_nacimiento': conductor.fecha_nacimiento.strftime('%Y-%m-%d'),
                'edad': conductor.get_edad(),
                'email': conductor.user.email,
                'telefono_principal': conductor.telefono_principal,
                'telefono_secundario': conductor.telefono_secundario,
                'direccion': conductor.direccion,
                'ciudad': conductor.ciudad,
                'numero_licencia': conductor.numero_licencia,
                'licencia_expedicion': conductor.licencia_expedicion.strftime('%Y-%m-%d'),
                'licencia_vencimiento': conductor.licencia_vencimiento.strftime('%Y-%m-%d'),
                'tipo_cuenta': conductor.tipo_cuenta,
                'banco': conductor.banco,
                'numero_cuenta': conductor.numero_cuenta,
                'estado': conductor.estado,
                'vehiculo': vehiculo_data,
                'activo': conductor.activo,
                'fecha_registro': conductor.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'success': True,
            'count': len(conductores_data),
            'data': conductores_data
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al consultar conductores: {str(e)}'
        }, status=500)
