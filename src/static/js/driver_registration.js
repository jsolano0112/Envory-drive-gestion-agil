// ====================================
// VALIDACIÓN Y MENSAJES (FUNCIONES GLOBALES)
// ====================================

function showMessage(message, type) {
    const messageContainer = document.getElementById("messageContainer");
    const bgColor =
        type === "success"
            ? "bg-green-100 border-green-500 text-green-700"
            : "bg-red-100 border-red-500 text-red-700";

    const formattedMessage = message.replace(/\n/g, '<br>');

    messageContainer.innerHTML = `
        <div class="${bgColor} border-l-4 p-4 rounded shadow-lg" role="alert">
            <div class="flex">
                <div class="flex-shrink-0">
                    ${type === "success"
            ? '<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>'
            : '<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>'
        }
                </div>
                <div class="ml-3">
                    <p class="font-semibold">${formattedMessage}</p>
                </div>
            </div>
        </div>
    `;

    messageContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });

    setTimeout(() => {
        messageContainer.innerHTML = "";
    }, 8000);
}

function validatePassword(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    return (
        password.length >= minLength &&
        hasUpperCase &&
        hasLowerCase &&
        hasNumber &&
        hasSpecialChar
    );
}

function validateForm() {
    const allInputs = document.querySelectorAll("[required]");
    let isValid = true;
    let missingFields = [];

    allInputs.forEach((input) => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add("border-red-500");

            const label = input.previousElementSibling;
            if (label && label.tagName === 'LABEL') {
                const fieldName = label.textContent.replace('*', '').trim();
                missingFields.push(fieldName);
            }
        } else {
            input.classList.remove("border-red-500");
        }
    });

    const requiredFiles = document.querySelectorAll('input[type="file"][required]');
    requiredFiles.forEach((fileInput) => {
        if (!fileInput.files || fileInput.files.length === 0) {
            isValid = false;
            fileInput.classList.add("border-red-500");

            const label = fileInput.closest('div').querySelector('label');
            if (label) {
                const fieldName = label.textContent.replace('*', '').trim();
                missingFields.push(fieldName);
            }
        } else {
            fileInput.classList.remove("border-red-500");
        }
    });

    if (!isValid) {
        let errorMessage = "Error: faltan campos obligatorios:\n";
        errorMessage += missingFields.join(", ");
        showMessage(errorMessage, "error");
        goToFirstTabWithErrors();
        return false;
    }

    const passwordInput = document.querySelector('[name="password"]');
    const confirmPasswordInput = document.querySelector('[name="confirm_password"]');

    if (passwordInput.value !== confirmPasswordInput.value) {
        showMessage("Las contraseñas no coinciden", "error");
        return false;
    }

    const numeroCuenta = document.querySelector('[name="numero_cuenta"]');
    const confirmarCuenta = document.querySelector('[name="confirmar_numero_cuenta"]');

    if (numeroCuenta.value !== confirmarCuenta.value) {
        showMessage("Los números de cuenta no coinciden", "error");
        return false;
    }

    const fechaNacimiento = document.querySelector('[name="fecha_nacimiento"]');
    if (fechaNacimiento && fechaNacimiento.value) {
        const birthDate = new Date(fechaNacimiento.value);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        if (age < 21) {
            showMessage("El conductor debe ser mayor de 21 años", "error");
            return false;
        }
    }

    const licenciaExpedicion = document.querySelector('[name="licencia_expedicion"]');
    const licenciaVencimiento = document.querySelector('[name="licencia_vencimiento"]');

    if (licenciaExpedicion && licenciaVencimiento &&
        licenciaExpedicion.value && licenciaVencimiento.value) {

        const expedicion = new Date(licenciaExpedicion.value);
        const vencimiento = new Date(licenciaVencimiento.value);
        const today = new Date();

        if (vencimiento <= expedicion) {
            showMessage("La fecha de vencimiento debe ser posterior a la fecha de expedición", "error");
            return false;
        }

        if (vencimiento <= today) {
            showMessage("La licencia de conducción está vencida", "error");
            return false;
        }
    }

    const anioVehiculo = document.querySelector('[name="anio"]');
    if (anioVehiculo && anioVehiculo.value) {
        const anio = parseInt(anioVehiculo.value);
        const currentYear = new Date().getFullYear();

        if (anio < 2015 || anio > currentYear) {
            showMessage("El año del vehículo debe estar entre 2015 y el año actual", "error");
            return false;
        }
    }

    const placa = document.querySelector('[name="placa"]');
    if (placa && placa.value) {
        const value = placa.value.toUpperCase();

        // Solo letras o números, máximo 6 caracteres
        const basicPattern = /^[A-Z0-9]{1,6}$/;
        if (!basicPattern.test(value)) {
            showMessage("La placa solo puede tener letras o números (máximo 6 caracteres)", "error");
            return false;
        }

        // Contar letras y números
        const letters = (value.match(/[A-Z]/g) || []).length;
        const digits = (value.match(/[0-9]/g) || []).length;

        // Validar que tenga al menos dos letras o dos números
        if (letters < 2 && digits < 2) {
            showMessage("La placa debe tener al menos dos letras o dos números", "error");
            return false;
        }
    }


    return true;
}

function goToFirstTabWithErrors() {
    const tabContents = document.querySelectorAll(".tab-content");
    const tabs = document.querySelectorAll(".tab-button");

    for (let i = 0; i < tabContents.length; i++) {
        const tabContent = tabContents[i];
        const requiredInputs = tabContent.querySelectorAll("[required]");
        const requiredFiles = tabContent.querySelectorAll('input[type="file"][required]');

        let hasErrors = false;

        requiredInputs.forEach((input) => {
            if (!input.value.trim()) {
                hasErrors = true;
            }
        });

        requiredFiles.forEach((fileInput) => {
            if (!fileInput.files || fileInput.files.length === 0) {
                hasErrors = true;
            }
        });

        if (hasErrors) {
            // Trigger the tab click
            tabs[i].click();
            break;
        }
    }
}

// ====================================
// ENVÍO DEL FORMULARIO (FUNCIÓN GLOBAL)
// ====================================

async function submitDriverForm(event) {
    event.preventDefault();

    console.log('Validando formulario...');

    if (!validateForm()) {
        return;
    }

    const submitBtn = document.getElementById("submitBtn");
    const originalText = submitBtn.textContent;
    submitBtn.textContent = "Registrando...";
    submitBtn.disabled = true;

    try {
        const formData = new FormData(document.getElementById("driverForm"));

        const response = await fetch('/api/conductores/registro/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });

        const data = await response.json();

        if (data.success) {
            showMessage(data.message, "success");

            setTimeout(() => {
                window.location.href = '/accounts/login/';
            }, 3000);
        } else {
            showMessage(data.message || "Error al procesar el registro", "error");
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage("Error al procesar el registro. Intente nuevamente.", "error");
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// ====================================
// INICIALIZACIÓN
// ====================================

document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const submitBtn = document.getElementById("submitBtn");
    let currentTab = 0;

    function showTab(index) {
        tabContents.forEach((content) => content.classList.add("hidden"));
        tabs.forEach((tab) => {
            tab.classList.remove("tab-active");
            tab.classList.add("tab-inactive");
        });

        tabContents[index].classList.remove("hidden");
        tabs[index].classList.add("tab-active");
        tabs[index].classList.remove("tab-inactive");

        prevBtn.disabled = index === 0;

        if (index === tabs.length - 1) {
            nextBtn.classList.add("hidden");
            submitBtn.classList.remove("hidden");
        } else {
            nextBtn.classList.remove("hidden");
            submitBtn.classList.add("hidden");
        }
    }

    function validateCurrentTab() {
        const currentContent = tabContents[currentTab];
        const requiredInputs = currentContent.querySelectorAll("[required]");
        let isValid = true;

        requiredInputs.forEach((input) => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add("border-red-500");
            } else {
                input.classList.remove("border-red-500");
            }
        });

        if (!isValid) {
            showMessage("Por favor complete todos los campos obligatorios", "error");
        }

        return isValid;
    }

    // Tab navigation
    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            currentTab = index;
            showTab(index);
        });
    });

    prevBtn.addEventListener("click", () => {
        if (currentTab > 0) {
            currentTab--;
            showTab(currentTab);
        }
    });

    nextBtn.addEventListener("click", () => {
        if (validateCurrentTab()) {
            if (currentTab < tabs.length - 1) {
                currentTab++;
                showTab(currentTab);
            }
        }
    });

    // Password validation
    const passwordInput = document.querySelector('[name="password"]');
    const confirmPasswordInput = document.querySelector('[name="confirm_password"]');

    passwordInput.addEventListener("blur", function () {
        if (!validatePassword(this.value)) {
            this.classList.add("border-red-500");
            showMessage(
                "La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial",
                "error"
            );
        } else {
            this.classList.remove("border-red-500");
        }
    });

    confirmPasswordInput.addEventListener("blur", function () {
        if (this.value !== passwordInput.value) {
            this.classList.add("border-red-500");
            showMessage("Las contraseñas no coinciden", "error");
        } else {
            this.classList.remove("border-red-500");
        }
    });

    // Age validation
    const fechaNacimiento = document.querySelector('[name="fecha_nacimiento"]');
    fechaNacimiento.addEventListener("change", function () {
        const birthDate = new Date(this.value);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        if (age < 21) {
            this.classList.add("border-red-500");
            showMessage("El conductor debe ser mayor de 21 años", "error");
        } else {
            this.classList.remove("border-red-500");
        }
    });

    // Plate format validation
    const placaInput = document.querySelector('[name="placa"]');
    placaInput.addEventListener("input", function () {
        this.value = this.value.toUpperCase();
    });

    // Bank account confirmation
    const numeroCuenta = document.querySelector('[name="numero_cuenta"]');
    const confirmarCuenta = document.querySelector('[name="confirmar_numero_cuenta"]');

    confirmarCuenta.addEventListener("blur", function () {
        if (this.value !== numeroCuenta.value) {
            this.classList.add("border-red-500");
            showMessage("Los números de cuenta no coinciden", "error");
        } else {
            this.classList.remove("border-red-500");
        }
    });

    // File upload preview
    document.querySelectorAll('input[type="file"]').forEach((input) => {
        input.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                if (file.size > 5 * 1024 * 1024) {
                    showMessage("El archivo es demasiado grande. Máximo 5MB", "error");
                    this.value = "";
                    return;
                }

                const label = this.parentElement.querySelector("label");
                const fileName = file.name;
                label.querySelector("p.text-sm").textContent = fileName;
                label.querySelector("p.text-sm").classList.add("text-green-600", "font-semibold");
            }
        });
    });

    // IMPORTANTE: Event listener del formulario
    const driverForm = document.getElementById("driverForm");
    if (driverForm) {
        driverForm.addEventListener("submit", submitDriverForm);
    }

    // Cancel button
    const cancelBtn = document.getElementById("cancelBtn");
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function (e) {
            e.preventDefault();
            if (confirm("¿Está seguro que desea cancelar el registro? Se perderán todos los datos ingresados.")) {
                window.location.href = '/accounts/login/';
            }
        });
    }

    // Initialize
    showTab(0);
});