"""
Script para crear datos de prueba para el módulo de registro de clientes.
Ejecutar: python crear_datos_prueba.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evory_drive.settings')
django.setup()

from src.models import Compania, Cliente
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
        
        print("\n" + "=" * 60)
        print("DATOS DE PRUEBA CREADOS EXITOSAMENTE")
        print("=" * 60)
        print("\nRESUMEN:")
        print(f"   Compañías activas: {Compania.objects.filter(estado=True).count()}")
        print(f"   Clientes registrados: {Cliente.objects.count()}")
        print("\nSiguiente paso:")
        print("   Accede a: http://127.0.0.1:8000/registro-cliente/")
        print("   O prueba login con: prueba@evory.com / Prueba123")
        print()
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

