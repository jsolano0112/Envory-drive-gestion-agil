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

from .models import Cliente, Compania

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
