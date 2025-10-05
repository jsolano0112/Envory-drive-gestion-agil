
// Tab functionality
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

    // Update buttons
    prevBtn.disabled = index === 0;

    if (index === tabs.length - 1) {
        nextBtn.classList.add("hidden");
        submitBtn.classList.remove("hidden");
    } else {
        nextBtn.classList.remove("hidden");
        submitBtn.classList.add("hidden");
    }
}

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

// Validation function
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
        showMessage(
            "Por favor complete todos los campos obligatorios",
            "error"
        );
    }

    return isValid;
}

// Password validation
const passwordInput = document.querySelector('[name="password"]');
const confirmPasswordInput = document.querySelector(
    '[name="confirm_password"]'
);

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
const fechaNacimiento = document.querySelector(
    '[name="fecha_nacimiento"]'
);
fechaNacimiento.addEventListener("change", function () {
    const birthDate = new Date(this.value);
    const today = new Date();
    const age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();

    if (
        monthDiff < 0 ||
        (monthDiff === 0 && today.getDate() < birthDate.getDate())
    ) {
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
const confirmarCuenta = document.querySelector(
    '[name="confirmar_numero_cuenta"]'
);

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
            // Validate file size (5MB max)
            if (file.size > 5 * 1024 * 1024) {
                showMessage(
                    "El archivo es demasiado grande. Máximo 5MB",
                    "error"
                );
                this.value = "";
                return;
            }

            const label = this.parentElement.querySelector("label");
            const fileName = file.name;
            label.querySelector("p.text-sm").textContent = fileName;
            label
                .querySelector("p.text-sm")
                .classList.add("text-green-600", "font-semibold");
        }
    });
});

// Save draft functionality
document
    .getElementById("saveDraftBtn")
    .addEventListener("click", function () {
        showMessage("Borrador guardado exitosamente", "success");
        // Here you would implement the actual save draft logic
    });

// Form submission
document
    .getElementById("driverForm")
    .addEventListener("submit", function (e) {
        e.preventDefault();

        if (validateForm()) {
            // Here you would send the form data to Django backend
            showMessage(
                "El registro del conductor fue exitoso. Estado: Pendiente de Verificación",
                "success"
            );

            // Simulate form submission
            setTimeout(() => {
                this.submit();
            }, 2000);
        }
    });

function validateForm() {
    // Validate all required fields
    const allInputs = document.querySelectorAll("[required]");
    let isValid = true;

    allInputs.forEach((input) => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add("border-red-500");
        }
    });

    if (!isValid) {
        showMessage("Error: faltan campos obligatorios", "error");
        return false;
    }

    // Validate passwords match
    if (passwordInput.value !== confirmPasswordInput.value) {
        showMessage("Las contraseñas no coinciden", "error");
        return false;
    }

    // Validate bank account numbers match
    if (numeroCuenta.value !== confirmarCuenta.value) {
        showMessage("Los números de cuenta no coinciden", "error");
        return false;
    }

    return true;
}

function showMessage(message, type) {
    const messageContainer = document.getElementById("messageContainer");
    const bgColor =
        type === "success"
            ? "bg-green-100 border-green-500 text-green-700"
            : "bg-red-100 border-red-500 text-red-700";

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
                            <p class="font-semibold">${message}</p>
                        </div>
                    </div>
                </div>
            `;

    setTimeout(() => {
        messageContainer.innerHTML = "";
    }, 5000);
}

// Initialize
showTab(0);