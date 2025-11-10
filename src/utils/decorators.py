from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps

def get_user_type(user):
    """
    Determina el tipo de usuario basado en sus relaciones.
    Retorna: 'admin', 'cliente', 'conductor'
    """
    if hasattr(user, 'cliente') and user.cliente:
        return 'cliente'
    elif hasattr(user, 'conductor') and user.conductor:
        return 'conductor'
    else:
        return 'admin'

def admin_required(view_func):
    """
    Decorador que verifica que el usuario sea administrador 
    (no pertenezca a Cliente ni Conductor).
    Si no es admin, redirige al home con mensaje de error.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        # 🔴 CORRECCIÓN: La lógica estaba al revés
        es_cliente = hasattr(request.user, 'cliente') and request.user.cliente
        es_conductor = hasattr(request.user, 'conductor') and request.user.conductor
        
        # Si NO es cliente NI conductor, entonces es admin y puede acceder
        if not es_cliente and not es_conductor:
            return view_func(request, *args, **kwargs)
        
        # Si llega aquí, es cliente o conductor, no puede acceder
        messages.error(request, 'No tienes permisos para acceder a esta sección. Solo los administradores pueden acceder.')
        return redirect('home')
    
    return wrapper

def cliente_required(view_func):
    """
    Decorador que verifica que el usuario sea cliente.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'cliente') and request.user.cliente:
            return view_func(request, *args, **kwargs)
        
        messages.warning(request, 'No tienes permisos para acceder a este módulo.')
        return redirect('home')
    
    return wrapper

def conductor_required(view_func):
    """
    Decorador que verifica que el usuario sea conductor.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'conductor') and request.user.conductor:
            return view_func(request, *args, **kwargs)
        
        messages.warning(request, 'No tienes permisos para acceder a este módulo.')
        return redirect('home')
    
    return wrapper