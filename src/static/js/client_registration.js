// ====================================
// MÓDULO: REGISTRO DE CLIENTES
// ====================================

// Elementos del DOM
const form = document.getElementById('clientForm');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');
const messageContainer = document.getElementById('messageContainer');

// Campos del formulario
const primerNombre = document.getElementById('primer_nombre');
const segundoNombre = document.getElementById('segundo_nombre');
const primerApellido = document.getElementById('primer_apellido');
const segundoApellido = document.getElementById('segundo_apellido');
const tipoDocumento = document.getElementById('tipo_documento');
const numeroDocumento = document.getElementById('numero_documento');
const correo = document.getElementById('correo');
const telefono = document.getElementById('telefono');
const companiaId = document.getElementById('compania_id');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm_password');

// ====================================
// VALIDACIONES DE CAMPOS
// ====================================

/**
 * Valida que el texto solo contenga letras y espacios (sin números ni símbolos)
 */
function validateNameField(value) {
    const namePattern = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;
    return namePattern.test(value);
}

/**
 * Valida formato de email
 */
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

/**
 * Valida contraseña: mínimo 8 caracteres, mayúscula, minúscula, número
 */
function validatePassword(pwd) {
    if (pwd.length < 8) return false;
    if (!/[A-Z]/.test(pwd)) return false;
    if (!/[a-z]/.test(pwd)) return false;
    if (!/\d/.test(pwd)) return false;
    return true;
}

/**
 * Valida que el número de documento solo contenga dígitos
 */
function validateNumeroDocumento(value) {
    return /^[0-9]+$/.test(value);
}

/**
 * Valida que el teléfono tenga 10 dígitos
 */
function validateTelefono(value) {
    return /^[0-9]{10}$/.test(value);
}

/**
 * Muestra error en un campo específico
 */
function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(`error_${fieldId}`);
    
    if (field) {
        field.classList.add('border-red-500');
        field.classList.remove('border-gray-300');
    }
    
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
    }
}

/**
 * Limpia error en un campo específico
 */
function clearFieldError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(`error_${fieldId}`);
    
    if (field) {
        field.classList.remove('border-red-500');
        field.classList.add('border-gray-300');
    }
    
    if (errorElement) {
        errorElement.classList.add('hidden');
        errorElement.textContent = '';
    }
}

/**
 * Limpia todos los errores
 */
function clearAllErrors() {
    const allFields = [
        'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
        'tipo_documento', 'numero_documento', 'correo', 'telefono',
        'compania_id', 'password', 'confirm_password'
    ];
    
    allFields.forEach(fieldId => clearFieldError(fieldId));
}

// ====================================
// VALIDACIONES EN TIEMPO REAL
// ====================================

// Validación de nombres (solo letras)
[primerNombre, segundoNombre, primerApellido, segundoApellido].forEach(field => {
    field.addEventListener('input', function() {
        const value = this.value.trim();
        if (value && !validateNameField(value)) {
            showFieldError(this.id, 'Solo se permiten letras y espacios');
        } else {
            clearFieldError(this.id);
        }
    });
});

// Validación de número de documento (solo números)
numeroDocumento.addEventListener('input', function() {
    const value = this.value.trim();
    if (value && !validateNumeroDocumento(value)) {
        showFieldError(this.id, 'Solo se permiten números');
    } else {
        clearFieldError(this.id);
    }
});

// Validación de correo
correo.addEventListener('blur', function() {
    const value = this.value.trim();
    if (value && !validateEmail(value)) {
        showFieldError(this.id, 'Verificar correo');
    } else {
        clearFieldError(this.id);
    }
});

// Validación de teléfono
telefono.addEventListener('input', function() {
    const value = this.value.trim();
    if (value && !validateTelefono(value)) {
        showFieldError(this.id, 'El teléfono debe tener 10 dígitos');
    } else {
        clearFieldError(this.id);
    }
});

// Validación de contraseña
password.addEventListener('blur', function() {
    const value = this.value;
    if (value && !validatePassword(value)) {
        showFieldError(this.id, 'La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula y un número');
    } else {
        clearFieldError(this.id);
    }
});

// Validación de confirmación de contraseña
confirmPassword.addEventListener('blur', function() {
    if (this.value !== password.value) {
        showFieldError(this.id, 'Las contraseñas no coinciden');
    } else {
        clearFieldError(this.id);
    }
});

// ====================================
// MENSAJES AL USUARIO
// ====================================

/**
 * Muestra un mensaje al usuario
 */
function showMessage(message, type = 'error') {
    const bgColor = type === 'success' 
        ? 'bg-green-100 border-green-500 text-green-700'
        : type === 'warning'
        ? 'bg-yellow-100 border-yellow-500 text-yellow-700'
        : 'bg-red-100 border-red-500 text-red-700';
    
    const icon = type === 'success'
        ? '<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>'
        : '<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>';
    
    messageContainer.innerHTML = `
        <div class="${bgColor} border-l-4 p-4 rounded shadow-lg" role="alert">
            <div class="flex">
                <div class="flex-shrink-0">
                    ${icon}
                </div>
                <div class="ml-3">
                    <p class="font-semibold">${message}</p>
                </div>
            </div>
        </div>
    `;
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        messageContainer.innerHTML = '';
    }, 5000);
    
    // Scroll hacia el mensaje
    messageContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ====================================
// CARGAR COMPAÑÍAS
// ====================================

/**
 * Carga la lista de compañías desde el backend
 */
async function loadCompanies() {
    try {
        const response = await fetch('/api/companias/');
        const result = await response.json();
        
        if (result.success) {
            companiaId.innerHTML = '<option value="">Seleccione una compañía...</option>';
            
            result.data.forEach(company => {
                const option = document.createElement('option');
                option.value = company.id;
                option.textContent = company.nombre;
                companiaId.appendChild(option);
            });
        } else {
            companiaId.innerHTML = '<option value="">Error al cargar compañías</option>';
            showMessage('No se pudieron cargar las compañías', 'error');
        }
    } catch (error) {
        console.error('Error al cargar compañías:', error);
        companiaId.innerHTML = '<option value="">Error al cargar compañías</option>';
        showMessage('Error de conexión al cargar compañías', 'error');
    }
}

// ====================================
// ENVÍO DEL FORMULARIO
// ====================================

/**
 * Valida todos los campos antes de enviar
 */
function validateForm() {
    clearAllErrors();
    let isValid = true;
    
    // Validar campos obligatorios
    if (!primerNombre.value.trim()) {
        showFieldError('primer_nombre', 'Este campo es obligatorio');
        isValid = false;
    } else if (!validateNameField(primerNombre.value.trim())) {
        showFieldError('primer_nombre', 'Solo se permiten letras y espacios');
        isValid = false;
    }
    
    if (!primerApellido.value.trim()) {
        showFieldError('primer_apellido', 'Este campo es obligatorio');
        isValid = false;
    } else if (!validateNameField(primerApellido.value.trim())) {
        showFieldError('primer_apellido', 'Solo se permiten letras y espacios');
        isValid = false;
    }
    
    // Validar nombres opcionales si están llenos
    if (segundoNombre.value.trim() && !validateNameField(segundoNombre.value.trim())) {
        showFieldError('segundo_nombre', 'Solo se permiten letras y espacios');
        isValid = false;
    }
    
    if (segundoApellido.value.trim() && !validateNameField(segundoApellido.value.trim())) {
        showFieldError('segundo_apellido', 'Solo se permiten letras y espacios');
        isValid = false;
    }
    
    if (!tipoDocumento.value) {
        showFieldError('tipo_documento', 'Debe seleccionar un tipo de documento');
        isValid = false;
    }
    
    if (!numeroDocumento.value.trim()) {
        showFieldError('numero_documento', 'Este campo es obligatorio');
        isValid = false;
    } else if (!validateNumeroDocumento(numeroDocumento.value.trim())) {
        showFieldError('numero_documento', 'Solo se permiten números');
        isValid = false;
    }
    
    if (!correo.value.trim()) {
        showFieldError('correo', 'Este campo es obligatorio');
        isValid = false;
    } else if (!validateEmail(correo.value.trim())) {
        showFieldError('correo', 'Verificar correo');
        isValid = false;
    }
    
    if (!telefono.value.trim()) {
        showFieldError('telefono', 'Este campo es obligatorio');
        isValid = false;
    } else if (!validateTelefono(telefono.value.trim())) {
        showFieldError('telefono', 'El teléfono debe tener 10 dígitos');
        isValid = false;
    }
    
    if (!companiaId.value) {
        showFieldError('compania_id', 'Debe seleccionar una compañía');
        isValid = false;
    }
    
    if (!password.value) {
        showFieldError('password', 'Este campo es obligatorio');
        isValid = false;
    } else if (!validatePassword(password.value)) {
        showFieldError('password', 'La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula y un número');
        isValid = false;
    }
    
    if (!confirmPassword.value) {
        showFieldError('confirm_password', 'Este campo es obligatorio');
        isValid = false;
    } else if (password.value !== confirmPassword.value) {
        showFieldError('confirm_password', 'Las contraseñas no coinciden');
        isValid = false;
    }
    
    if (!isValid) {
        showMessage('Error: faltan campos obligatorios', 'error');
    }
    
    return isValid;
}

/**
 * Envía el formulario al backend
 */
async function submitForm(event) {
    event.preventDefault();
    
    // Validar formulario
    if (!validateForm()) {
        return;
    }
    
    // Deshabilitar botón de envío
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registrando...';
    
    try {
        // Preparar datos
        const formData = {
            primer_nombre: primerNombre.value.trim(),
            segundo_nombre: segundoNombre.value.trim(),
            primer_apellido: primerApellido.value.trim(),
            segundo_apellido: segundoApellido.value.trim(),
            tipo_documento: tipoDocumento.value,
            numero_documento: numeroDocumento.value.trim(),
            correo: correo.value.trim(),
            telefono: telefono.value.trim(),
            compania_id: parseInt(companiaId.value),
            password: password.value,
            confirm_password: confirmPassword.value
        };
        
        // Enviar al backend
        const response = await fetch('/api/clientes/registro/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage(result.message, 'success');
            
            // Limpiar formulario
            form.reset();
            clearAllErrors();
            
            // Redirigir al login después de 2 segundos
            setTimeout(() => {
                window.location.href = '/accounts/login/';
            }, 2000);
        } else {
            showMessage(result.message, 'error');
        }
    } catch (error) {
        console.error('Error al enviar formulario:', error);
        showMessage('Error de conexión. Por favor intente nuevamente.', 'error');
    } finally {
        // Rehabilitar botón
        submitBtn.disabled = false;
        submitBtn.textContent = 'Registrar Cliente';
    }
}

// ====================================
// EVENT LISTENERS
// ====================================

form.addEventListener('submit', submitForm);

cancelBtn.addEventListener('click', function() {
    if (confirm('¿Está seguro que desea cancelar el registro?')) {
        window.location.href = '/';
    }
});

// ====================================
// INICIALIZACIÓN
// ====================================

// Cargar compañías al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    loadCompanies();
});

