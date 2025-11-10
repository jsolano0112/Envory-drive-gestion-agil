"""
Script para crear datos de prueba para el módulo de registro de clientes.
Ejecutar: python crear_datos_prueba.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evory_drive.settings')
django.setup()

from src.models.models import Compania, Cliente
from django.contrib.auth.models import User

def crear_companias():
    """Crea compañías de prueba"""
    print("\nCreando compañías de prueba...")
    
    companias_data = [
        {"nombre": "Transportes Unidos S.A.", "nit": "900123456-7"},
        {"nombre": "Corporación Movil Express", "nit": "900234567-8"},
        {"nombre": "Logística Global LTDA", "nit": "900345678-9"},
        {"nombre": "Empresa de Servicios ABC", "nit": "900456789-0"},
        {"nombre": "Grupo Empresarial XYZ", "nit": "900567890-1"},
    ]
    
    companias_creadas = []
    for data in companias_data:
        compania, created = Compania.objects.get_or_create(
            nombre=data["nombre"],
            defaults={"nit": data["nit"], "estado": True}
        )
        if created:
            companias_creadas.append(compania)
            print(f"  [OK] Creada: {compania.nombre}")
        else:
            if not compania.estado:
                compania.estado = True
                compania.save(update_fields=["estado"])
                print(f"  [FIX] Activada: {compania.nombre}")
            else:
                print(f"  [SKIP] Ya existe: {compania.nombre}")
    
    return companias_creadas


def crear_cliente_prueba():
    """Crea un cliente de prueba"""
    print("\nCreando cliente de prueba...")
    
    # Verificar si el usuario ya existe
    if User.objects.filter(email="prueba@evory.com").exists():
        print("  [SKIP] El cliente de prueba ya existe")
        return
    
    # Verificar que haya compañías
    companias = Compania.objects.filter(estado=True)
    if not companias.exists():
        print("  [ERROR] No hay compañías activas. Crea compañías primero.")
        return
    
    compania = companias.first()
    
    # Crear usuario
    user = User.objects.create_user(
        username="prueba@evory.com",
        email="prueba@evory.com",
        password="Prueba123",
        first_name="Juan",
        last_name="Pérez"
    )
    
    # Crear cliente
    cliente = Cliente.objects.create(
        user=user,
        segundo_nombre="Carlos",
        segundo_apellido="González",
        tipo_documento="CC",
        numero_documento="1234567890",
        telefono="3001234567",
        compania=compania
    )
    
    print(f"  [OK] Cliente creado: {cliente.get_nombre_completo()}")
    print("     Email: prueba@evory.com")
    print("     Password: Prueba123")
    print(f"     Compañía: {compania.nombre}")


def crear_conductores_prueba():
    """Crea conductores de prueba si no existen"""
    print("\nCreando conductores de prueba...")
    from src.models.models import Conductor, Vehiculo
    from datetime import date, timedelta
    
    if Conductor.objects.filter(activo=True).count() >= 3:
        print("  [SKIP] Ya hay conductores activos suficientes")
        return
    
    conductores_data = [
        {
            "email": "conductor1@evory.com",
            "first_name": "Carlos",
            "last_name": "Ramírez",
            "documento": "9876543210",
            "telefono": "3201234567",
            "licencia": "LIC001",
        },
        {
            "email": "conductor2@evory.com",
            "first_name": "María",
            "last_name": "González",
            "documento": "8765432109",
            "telefono": "3112345678",
            "licencia": "LIC002",
        },
        {
            "email": "conductor3@evory.com",
            "first_name": "Luis",
            "last_name": "Fernández",
            "documento": "7654321098",
            "telefono": "3123456789",
            "licencia": "LIC003",
        },
    ]
    
    for data in conductores_data:
        if User.objects.filter(email=data["email"]).exists():
            print(f"  [SKIP] Conductor ya existe: {data['email']}")
            continue
        
        # Crear usuario
        user = User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password="Conductor123",
            first_name=data["first_name"],
            last_name=data["last_name"]
        )
        
        # Crear conductor
        conductor = Conductor.objects.create(
            user=user,
            tipo_documento="CC",
            numero_documento=data["documento"],
            fecha_nacimiento=date.today() - timedelta(days=365*30),
            telefono_principal=data["telefono"],
            direccion="Calle 50 # 45-30, Medellín",
            ciudad="Medellín",
            numero_licencia=data["licencia"],
            licencia_expedicion=date.today() - timedelta(days=365*5),
            licencia_vencimiento=date.today() + timedelta(days=365*5),
            tipo_cuenta="Ahorros",
            banco="Bancolombia",
            numero_cuenta="1234567890",
            activo=True
        )
        
        # Crear vehículo
        Vehiculo.objects.create(
            conductor=conductor,
            placa=f"ABC{data['documento'][-3:]}",
            marca="Toyota",
            modelo="Corolla",
            anio=2020,
            color="Blanco",
            tipo_vehiculo="Sedan",
            num_pasajeros=4,
            activo=True
        )
        
        print(f"  [OK] Conductor creado: {conductor.get_nombre_completo()}")


def crear_viajes_para_clientes():
    """Crea viajes de prueba para todos los clientes"""
    print("\nCreando viajes para clientes...")
    from src.models.models import Conductor, Viaje
    from datetime import datetime, timedelta
    import random
    
    clientes = Cliente.objects.all()
    conductores = Conductor.objects.filter(activo=True)
    
    if conductores.count() == 0:
        print("  [ERROR] No hay conductores. Crea conductores primero.")
        return
    
    if clientes.count() == 0:
        print("  [ERROR] No hay clientes.")
        return
    
    origenes = [
        "Aeropuerto José María Córdova",
        "Centro Comercial Santa Fe",
        "Parque Lleras",
        "Terminal del Sur",
        "Universidad de Antioquia"
    ]
    
    destinos = [
        "Centro Empresarial Los Molinos",
        "Clínica Las Américas",
        "Hotel Dann Carlton",
        "Edificio Coltejer",
        "Plaza Mayor"
    ]
    
    estados = ['Completado', 'Completado', 'Completado', 'En Progreso', 'Cancelado']
    
    viajes_creados = 0
    for cliente in clientes:
        # Crear entre 8 y 15 viajes por cliente
        num_viajes = random.randint(8, 15)
        
        for _ in range(num_viajes):
            conductor = random.choice(conductores)
            estado = random.choice(estados)
            
            # Fecha aleatoria en los últimos 90 días
            dias_atras = random.randint(0, 90)
            fecha_solicitud = datetime.now() - timedelta(days=dias_atras, hours=random.randint(0, 23))
            
            viaje_data = {
                'cliente': cliente,
                'conductor': conductor,
                'fecha_solicitud': fecha_solicitud,
                'estado': estado,
                'origen': random.choice(origenes),
                'destino': random.choice(destinos),
                'valor_base': random.uniform(15000, 50000),
                'valor_adicional': random.uniform(0, 10000),
                'descuento': 0,
                'metodo_pago': random.choice(['Efectivo', 'Tarjeta', 'App'])
            }
            
            viaje_data['valor_total'] = viaje_data['valor_base'] + viaje_data['valor_adicional'] - viaje_data['descuento']
            
            if estado == 'Completado':
                viaje_data['fecha_inicio'] = fecha_solicitud + timedelta(minutes=random.randint(5, 30))
                viaje_data['fecha_fin'] = viaje_data['fecha_inicio'] + timedelta(minutes=random.randint(15, 60))
                viaje_data['calificacion_cliente'] = random.uniform(3.5, 5.0)
            
            Viaje.objects.create(**viaje_data)
            viajes_creados += 1
        
        print(f"  [OK] {num_viajes} viajes creados para {cliente.get_nombre_completo()}")
    
    print(f"\nTotal viajes creados: {viajes_creados}")


def main():
    """Función principal"""
    print("=" * 60)
    print("CREANDO DATOS DE PRUEBA - EVORY DRIVE")
    print("=" * 60)
    
    try:
        # Crear compañías
        crear_companias()
        
        # Crear cliente de prueba
        crear_cliente_prueba()
        
        # Crear conductores
        crear_conductores_prueba()
        
        # Crear viajes para todos los clientes
        crear_viajes_para_clientes()
        
        print("\n" + "=" * 60)
        print("DATOS DE PRUEBA CREADOS EXITOSAMENTE")
        print("=" * 60)
        print("\nRESUMEN:")
        print(f"   Compañías activas: {Compania.objects.filter(estado=True).count()}")
        print(f"   Clientes registrados: {Cliente.objects.count()}")
        from src.models.models import Conductor, Viaje
        print(f"   Conductores activos: {Conductor.objects.filter(activo=True).count()}")
        print(f"   Viajes totales: {Viaje.objects.count()}")
        print("\nSiguiente paso:")
        print("   Accede a: http://127.0.0.1:8000/companias/")
        print("   O http://127.0.0.1:8000/detalle-compania/2/")
        print()
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

