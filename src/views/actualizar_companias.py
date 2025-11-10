"""
Script para actualizar compañías existentes con los nuevos campos
y crear datos de prueba para el módulo de detalle de compañías.
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evory_drive.settings')
django.setup()

from django.contrib.auth.models import User
from src.models.models import Compania, Cliente, Conductor, Viaje, Novedad

def actualizar_companias():
    """Actualizar compañías existentes con datos completos"""
    print("\n=== ACTUALIZANDO COMPANIAS EXISTENTES ===")
    
    companias = Compania.objects.all()
    
    if companias.count() == 0:
        print("No hay compañías para actualizar. Creando compañías de prueba...")
        crear_companias_prueba()
        return
    
    for compania in companias:
        if not compania.razon_social:
            compania.razon_social = f"{compania.nombre} S.A.S."
        
        if not compania.direccion:
            direcciones = [
                "Calle 50 # 45-30, Medellín",
                "Carrera 43A # 1-50, Medellín",
                "Avenida El Poblado # 10-20, Medellín",
                "Calle 10 # 32-115, Medellín"
            ]
            compania.direccion = random.choice(direcciones)
        
        if not compania.telefono:
            compania.telefono = f"300{random.randint(1000000, 9999999)}"
        
        if not compania.email_corporativo:
            nombre_limpio = compania.nombre.lower().replace(' ', '').replace('ñ', 'n')
            compania.email_corporativo = f"contacto@{nombre_limpio}.com"
        
        if not compania.persona_contacto:
            nombres = ["María González", "Carlos Ramírez", "Ana Martínez", "Luis Pérez", "Diana Torres"]
            compania.persona_contacto = random.choice(nombres)
        
        if not compania.fecha_membresia:
            # Fecha aleatoria en los últimos 2 años
            dias_atras = random.randint(30, 730)
            compania.fecha_membresia = date.today() - timedelta(days=dias_atras)
        
        compania.save()
        print(f"Compañía actualizada: {compania.nombre}")
    
    print(f"\nTotal compañías actualizadas: {companias.count()}")


def crear_companias_prueba():
    """Crear compañías de prueba si no existen"""
    print("\n=== CREANDO COMPANIAS DE PRUEBA ===")
    
    companias_data = [
        {
            'nombre': 'TechCorp Solutions',
            'razon_social': 'TechCorp Solutions S.A.S.',
            'nit': '9001234567',
            'direccion': 'Calle 50 # 45-30, Medellín',
            'telefono': '3001234567',
            'email_corporativo': 'contacto@techcorp.com',
            'persona_contacto': 'María González',
            'fecha_membresia': date.today() - timedelta(days=365),
            'estado_cuenta': 'Activa'
        },
        {
            'nombre': 'Industrias del Norte',
            'razon_social': 'Industrias del Norte S.A.',
            'nit': '9007654321',
            'direccion': 'Carrera 43A # 1-50, Medellín',
            'telefono': '3007654321',
            'email_corporativo': 'info@industriasnorte.com',
            'persona_contacto': 'Carlos Ramírez',
            'fecha_membresia': date.today() - timedelta(days=180),
            'estado_cuenta': 'Activa'
        }
    ]
    
    for data in companias_data:
        compania, created = Compania.objects.get_or_create(
            nit=data['nit'],
            defaults=data
        )
        
        if created:
            print(f"Compañía creada: {compania.nombre}")
        else:
            # Actualizar campos
            for key, value in data.items():
                setattr(compania, key, value)
            compania.save()
            print(f"Compañía actualizada: {compania.nombre}")


def actualizar_clientes_con_cargo():
    """Asignar cargos a clientes existentes que no tienen"""
    print("\n=== ACTUALIZANDO CLIENTES CON CARGOS ===")
    
    clientes = Cliente.objects.filter(cargo__isnull=True) | Cliente.objects.filter(cargo='')
    
    cargos = [
        'Gerente General',
        'Director de Operaciones',
        'Analista de Sistemas',
        'Coordinador Logístico',
        'Asistente Administrativo',
        'Ingeniero de Proyectos',
        'Supervisor de Calidad',
        'Ejecutivo de Ventas'
    ]
    
    for cliente in clientes:
        cliente.cargo = random.choice(cargos)
        cliente.save()
        print(f"Cliente actualizado: {cliente.get_nombre_completo()} - {cliente.cargo}")
    
    print(f"\nTotal clientes actualizados: {clientes.count()}")


def crear_novedades_prueba():
    """Crear novedades de prueba"""
    print("\n=== CREANDO NOVEDADES DE PRUEBA ===")
    
    companias = Compania.objects.all()
    viajes = Viaje.objects.all()
    
    if companias.count() == 0 or viajes.count() == 0:
        print("No hay compañías o viajes. Saltando creación de novedades.")
        return
    
    # Obtener o crear usuario admin
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@evory.com', 'is_staff': True, 'is_superuser': True}
    )
    
    tipos_novedad = ['Retraso', 'Queja Cliente', 'Cambio de Ruta', 'Incidente']
    estados = ['Pendiente', 'En Revisión', 'Resuelta']
    prioridades = ['Media', 'Alta', 'Baja']
    
    novedades_creadas = 0
    for compania in companias:
        # Crear entre 3 y 8 novedades por compañía
        num_novedades = random.randint(3, 8)
        viajes_compania = viajes.filter(cliente__compania=compania)
        
        if viajes_compania.count() == 0:
            continue
        
        for _ in range(num_novedades):
            viaje = random.choice(viajes_compania)
            tipo = random.choice(tipos_novedad)
            estado = random.choice(estados)
            
            descripciones = {
                'Retraso': f'El conductor llegó con 20 minutos de retraso al punto de recogida.',
                'Queja Cliente': f'El cliente reportó que el vehículo no estaba en buenas condiciones.',
                'Cambio de Ruta': f'Se tuvo que cambiar la ruta debido a manifestaciones en el centro.',
                'Incidente': f'Incidente menor en la vía, sin heridos.'
            }
            
            dias_atras = random.randint(0, 60)
            fecha_creacion = datetime.now() - timedelta(days=dias_atras)
            
            novedad_data = {
                'compania': compania,
                'viaje': viaje,
                'conductor': viaje.conductor,
                'cliente': viaje.cliente,
                'tipo_novedad': tipo,
                'descripcion': descripciones[tipo],
                'estado': estado,
                'prioridad': random.choice(prioridades),
                'creado_por': admin_user
            }
            
            novedad = Novedad.objects.create(**novedad_data)
            novedad.fecha_creacion = fecha_creacion
            novedad.save()
            
            if estado == 'Resuelta':
                novedad.fecha_resolucion = fecha_creacion + timedelta(days=random.randint(1, 5))
                novedad.resolucion = "Novedad resuelta satisfactoriamente."
                novedad.resuelto_por = admin_user
                novedad.save()
            
            novedades_creadas += 1
    
    print(f"Total novedades creadas: {novedades_creadas}")


def main():
    print("\n" + "="*50)
    print("  ACTUALIZACION DE DATOS - MODULO DETALLE COMPANIAS")
    print("="*50)
    print("\nEste script actualiza información de compañías y clientes existentes.")
    print("Para crear conductores y viajes, ejecuta: python crear_datos_prueba.py")
    print("="*50 + "\n")
    
    actualizar_companias()
    actualizar_clientes_con_cargo()
    crear_novedades_prueba()
    
    print("\n" + "="*50)
    print("  ACTUALIZACION COMPLETADA EXITOSAMENTE")
    print("="*50)
    
    # Resumen final
    print("\n=== RESUMEN FINAL ===")
    print(f"Compañías: {Compania.objects.count()}")
    print(f"Clientes: {Cliente.objects.count()}")
    print(f"Conductores: {Conductor.objects.count()}")
    print(f"Viajes: {Viaje.objects.count()}")
    print(f"Novedades: {Novedad.objects.count()}")
    print("\n")
    print("NOTA: Si no hay viajes, ejecuta: python crear_datos_prueba.py")
    print("\n")


if __name__ == '__main__':
    main()

