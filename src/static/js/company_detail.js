// ====================================
// VARIABLES GLOBALES
// ====================================
let currentCompanyId = null;
let currentCompanyData = null;

// ====================================
// INICIALIZACIÓN
// ====================================
document.addEventListener('DOMContentLoaded', function() {
    // Obtener el ID de la compañía de la URL o del HTML
    currentCompanyId = document.getElementById('company-id').textContent.trim();
    
    // Cargar datos iniciales
    loadCompanyDetail();
    
    // Configurar event listeners
    setupEventListeners();
});

// ====================================
// CONFIGURACIÓN DE EVENT LISTENERS
// ====================================
function setupEventListeners() {
    // Pestañas
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });
    
    // Buscador de compañías
    const searchInput = document.getElementById('company-search');
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchCompanies(this.value);
        }, 300);
    });
    
    // Cerrar resultados de búsqueda al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#company-search') && !e.target.closest('#search-results')) {
            document.getElementById('search-results').classList.add('hidden');
        }
    });
    
    // Tipo de reporte
    document.getElementById('report-type').addEventListener('change', function() {
        updateReportDescription(this.value);
        validateReportForm();
    });
    
    // Fechas
    document.getElementById('fecha-inicio').addEventListener('change', validateReportForm);
    document.getElementById('fecha-fin').addEventListener('change', validateReportForm);
    
    // Botón de exportar a Excel
    document.getElementById('btn-export-excel').addEventListener('click', exportToExcel);
}

// ====================================
// GESTIÓN DE PESTAÑAS
// ====================================
function switchTab(tabName) {
    // Actualizar botones
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => {
        if (button.dataset.tab === tabName) {
            button.classList.add('active', 'border-blue-600', 'text-blue-600');
            button.classList.remove('border-transparent', 'text-gray-600');
        } else {
            button.classList.remove('active', 'border-blue-600', 'text-blue-600');
            button.classList.add('border-transparent', 'text-gray-600');
        }
    });
    
    // Actualizar contenido
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => {
        content.classList.add('hidden');
        content.classList.remove('active');
    });
    
    const activeContent = document.getElementById(`tab-${tabName}`);
    activeContent.classList.remove('hidden');
    activeContent.classList.add('active');
    
    // Cargar datos según la pestaña
    if (tabName === 'clientes') {
        loadClients();
    } else if (tabName === 'datos') {
        loadCompanyData();
    }
}

// ====================================
// BÚSQUEDA DE COMPAÑÍAS
// ====================================
async function searchCompanies(query) {
    if (query.length < 2) {
        document.getElementById('search-results').classList.add('hidden');
        return;
    }
    
    try {
        const response = await fetch(`/api/companias/buscar/?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success && data.data.length > 0) {
            displaySearchResults(data.data);
        } else {
            document.getElementById('search-results').innerHTML = '<p class="p-3 text-gray-600 text-sm">No se encontraron resultados</p>';
            document.getElementById('search-results').classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error en búsqueda:', error);
    }
}

function displaySearchResults(companies) {
    const resultsDiv = document.getElementById('search-results');
    resultsDiv.innerHTML = '';
    
    companies.forEach(company => {
        const item = document.createElement('div');
        item.className = 'p-3 hover:bg-gray-100 cursor-pointer border-b last:border-b-0';
        item.innerHTML = `
            <p class="font-semibold text-gray-800">${company.nombre}</p>
            <p class="text-xs text-gray-600">NIT: ${company.nit} | Estado: ${company.estado_cuenta}</p>
        `;
        item.addEventListener('click', () => {
            window.location.href = `/detalle-compania/${company.id}/`;
        });
        resultsDiv.appendChild(item);
    });
    
    resultsDiv.classList.remove('hidden');
}

// ====================================
// CARGAR DETALLE DE COMPAÑÍA
// ====================================
async function loadCompanyDetail() {
    try {
        const response = await fetch(`/api/companias/${currentCompanyId}/detalle/`);
        const data = await response.json();
        
        if (data.success) {
            currentCompanyData = data.data;
            updateMetrics(data.data.metricas);
            // Cargar clientes por defecto
            loadClients();
        } else {
            showNotification('Error al cargar los datos de la compañía', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al conectar con el servidor', 'error');
    }
}

function updateMetrics(metrics) {
    document.getElementById('metric-servicios').textContent = metrics.servicios_realizados;
    document.getElementById('metric-empleados').textContent = metrics.empleados_activos;
    document.getElementById('metric-mes').textContent = metrics.servicios_mes;
    
    const porcentaje = metrics.porcentaje_mes;
    const porcentajeElement = document.getElementById('metric-porcentaje');
    
    if (porcentaje >= 0) {
        porcentajeElement.innerHTML = `<span class="text-green-500"><i class="fas fa-arrow-up"></i> ${porcentaje}%</span> vs mes anterior`;
    } else {
        porcentajeElement.innerHTML = `<span class="text-red-500"><i class="fas fa-arrow-down"></i> ${Math.abs(porcentaje)}%</span> vs mes anterior`;
    }
}

// ====================================
// CARGAR CLIENTES ASOCIADOS
// ====================================
async function loadClients() {
    const container = document.getElementById('clientes-container');
    const loading = document.getElementById('loading-clientes');
    
    container.innerHTML = '';
    loading.classList.remove('hidden');
    
    try {
        const response = await fetch(`/api/companias/${currentCompanyId}/clientes/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        loading.classList.add('hidden');
        
        if (data.success) {
            document.getElementById('total-clientes').textContent = data.count;
            
            if (data.count === 0) {
                container.innerHTML = '<div class="text-center py-12"><i class="fas fa-users text-gray-300 text-6xl mb-4"></i><p class="text-gray-600 text-lg">No hay clientes registrados para esta compañía</p></div>';
                return;
            }
            
            data.data.forEach(cliente => {
                const card = createClientCard(cliente);
                container.appendChild(card);
            });
        } else {
            container.innerHTML = '<div class="text-center py-12"><i class="fas fa-exclamation-triangle text-red-500 text-6xl mb-4"></i><p class="text-gray-600 text-lg">Error al cargar clientes</p></div>';
            showNotification(data.message || 'Error al cargar clientes', 'error');
        }
    } catch (error) {
        loading.classList.add('hidden');
        console.error('Error completo:', error);
        container.innerHTML = `<div class="text-center py-12"><i class="fas fa-exclamation-circle text-red-500 text-6xl mb-4"></i><p class="text-gray-600 text-lg">Error al conectar con el servidor</p><p class="text-gray-500 text-sm mt-2">${error.message}</p></div>`;
        showNotification('Error al conectar con el servidor. Revisa la consola para más detalles.', 'error');
    }
}

function createClientCard(cliente) {
    const card = document.createElement('div');
    card.className = 'bg-white border-l-4 border-blue-500 rounded-lg p-6 hover:shadow-md transition-shadow mb-4';
    
    const statusClass = cliente.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
    const statusText = cliente.activo ? 'Activo' : 'Inactivo';
    const buttonClass = cliente.activo ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600';
    const buttonText = cliente.activo ? 'Desactivar' : 'Activar';
    
    // Manejar calificación (puede ser null o undefined)
    const calificacion = Number(cliente.calificacion_promedio) || 0;
    const calificacionTexto = typeof calificacion === 'number' && calificacion > 0 ? calificacion.toFixed(1) : '0.0';
    
    // Generar estrellas de calificación
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= Math.floor(calificacion)) {
            stars += '<i class="fas fa-star text-yellow-400"></i>';
        } else if (i === Math.ceil(calificacion) && calificacion % 1 !== 0) {
            stars += '<i class="fas fa-star-half-alt text-yellow-400"></i>';
        } else {
            stars += '<i class="far fa-star text-yellow-400"></i>';
        }
    }
    
    // Formatear fecha del último viaje
    let ultimoViajeTexto = 'Sin viajes registrados';
    if (cliente.ultimo_viaje && cliente.ultimo_viaje.fecha) {
        try {
            const fecha = new Date(cliente.ultimo_viaje.fecha);
            const fechaStr = fecha.toLocaleDateString('es-ES', { year: 'numeric', month: '2-digit', day: '2-digit' });
            const horaStr = fecha.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
            ultimoViajeTexto = `${fechaStr} - ${horaStr} - Último viaje`;
        } catch (e) {
            ultimoViajeTexto = cliente.ultimo_viaje.fecha + ' - Último viaje';
        }
    }
    
    card.innerHTML = `
        <div class="flex items-start justify-between">
            <!-- Indicador de estado -->
            <div class="flex items-center space-x-1 mr-4">
                <div class="w-3 h-3 rounded-full ${cliente.activo ? 'bg-green-500' : 'bg-red-500'}"></div>
            </div>
            
            <!-- Información Principal -->
            <div class="flex-1">
                <div class="flex items-start justify-between mb-3">
                    <div>
                        <h3 class="text-lg font-bold text-gray-800">${cliente.nombre_completo || 'Sin nombre'}</h3>
                        <p class="text-sm text-gray-600">Cliente: ${cliente.numero_documento || 'N/A'} | ${cliente.cargo || 'Sin cargo'}</p>
                    </div>
                    <span class="px-3 py-1 text-xs font-semibold rounded-full ${statusClass}">
                        ${statusText}
                    </span>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mb-3">
                    <div>
                        <p class="text-gray-600 font-medium">Origen:</p>
                        <p class="text-gray-800">${cliente.ultimo_viaje && cliente.ultimo_viaje.origen ? cliente.ultimo_viaje.origen : 'Sin viajes'}</p>
                    </div>
                    <div>
                        <p class="text-gray-600 font-medium">Viajes totales:</p>
                        <p class="text-gray-800 font-semibold">${cliente.total_viajes || 0}</p>
                    </div>
                    <div>
                        <p class="text-gray-600 font-medium">Calificación:</p>
                        <div class="flex items-center space-x-1">
                            ${stars}
                            <span class="text-gray-800 font-semibold ml-2">${calificacionTexto}</span>
                        </div>
                    </div>
                </div>
                
                <div class="flex items-center justify-between">
                    <p class="text-xs text-gray-500">
                        <i class="fas fa-clock mr-1"></i>
                        ${ultimoViajeTexto}
                    </p>
                    <button 
                        onclick="toggleClientStatus(${cliente.id}, ${!cliente.activo})"
                        class="${buttonClass} text-white px-6 py-2 rounded-lg text-sm font-semibold transition-colors"
                    >
                        ${buttonText}
                    </button>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// ====================================
// ACTIVAR/DESACTIVAR CLIENTE
// ====================================
async function toggleClientStatus(clientId, newStatus) {
    try {
        const response = await fetch(`/api/clientes/${clientId}/toggle-status/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ activo: newStatus })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            loadClients(); // Recargar la lista
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al actualizar el estado del cliente', 'error');
    }
}

// ====================================
// CARGAR DATOS DE LA EMPRESA
// ====================================
function loadCompanyData() {
    if (!currentCompanyData) return;
    
    document.getElementById('data-razon-social').textContent = currentCompanyData.razon_social || '-';
    document.getElementById('data-nit').textContent = currentCompanyData.nit || '-';
    document.getElementById('data-direccion').textContent = currentCompanyData.direccion || '-';
    document.getElementById('data-telefono').textContent = currentCompanyData.telefono || '-';
    document.getElementById('data-email').textContent = currentCompanyData.email_corporativo || '-';
    document.getElementById('data-contacto').textContent = currentCompanyData.persona_contacto || '-';
    document.getElementById('data-membresia').textContent = currentCompanyData.fecha_membresia ? 
        new Date(currentCompanyData.fecha_membresia).toLocaleDateString() : '-';
    
    const estadoCuenta = currentCompanyData.estado_cuenta;
    const estadoElement = document.getElementById('data-estado-cuenta');
    
    let colorClass = '';
    switch(estadoCuenta) {
        case 'Activa':
            colorClass = 'bg-green-100 text-green-800';
            break;
        case 'Suspendida':
            colorClass = 'bg-yellow-100 text-yellow-800';
            break;
        case 'Morosa':
            colorClass = 'bg-red-100 text-red-800';
            break;
        case 'Cancelada':
            colorClass = 'bg-gray-100 text-gray-800';
            break;
    }
    
    estadoElement.innerHTML = `<span class="px-3 py-1 rounded-full text-sm font-semibold ${colorClass}">${estadoCuenta}</span>`;
}

// ====================================
// GESTIÓN DE REPORTES
// ====================================
function updateReportDescription(reportType) {
    const descriptionDiv = document.getElementById('report-description');
    const descriptionText = document.getElementById('description-text');
    
    const descriptions = {
        'servicios': 'Este reporte incluye TODOS los viajes solicitados (completados, en progreso, cancelados, etc.) con: ID de cliente, nombre de cliente, empresa, ID empresa, fecha, ID conductor, nombre conductor, origen, destino y estado.',
        'ingresos': 'Este reporte incluye SOLO viajes completados con sus montos: ID viaje, fecha, ID empresa, nombre empresa, monto pagado, método de pago, origen y destino.',
        'novedades': 'Este reporte incluye todas las incidencias reportadas: quién la creó, descripción, tipo de novedad, estado actual, prioridad y fecha de resolución.'
    };
    
    if (reportType && descriptions[reportType]) {
        descriptionText.textContent = descriptions[reportType];
        descriptionDiv.classList.remove('hidden');
    } else {
        descriptionDiv.classList.add('hidden');
    }
}

function validateReportForm() {
    const reportType = document.getElementById('report-type').value;
    const fechaInicio = document.getElementById('fecha-inicio').value;
    const fechaFin = document.getElementById('fecha-fin').value;
    
    const isValid = reportType && fechaInicio && fechaFin;
    
    document.getElementById('btn-export-excel').disabled = !isValid;
    
    // Validar que fecha fin sea mayor a fecha inicio
    if (fechaInicio && fechaFin && fechaFin < fechaInicio) {
        showNotification('La fecha de fin debe ser posterior a la fecha de inicio', 'warning');
        document.getElementById('btn-export-excel').disabled = true;
    }
}

// ====================================
// EXPORTAR REPORTE A EXCEL
// ====================================
async function exportToExcel() {
    const reportType = document.getElementById('report-type').value;
    const fechaInicio = document.getElementById('fecha-inicio').value;
    const fechaFin = document.getElementById('fecha-fin').value;
    
    const endpoints = {
        'servicios': '/api/reportes/servicios/',
        'ingresos': '/api/reportes/ingresos/',
        'novedades': '/api/reportes/novedades/'
    };
    
    try {
        showNotification('Generando archivo Excel...', 'info');
        
        const response = await fetch(endpoints[reportType], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                company_id: currentCompanyId,
                fecha_inicio: fechaInicio,
                fecha_fin: fechaFin,
                export: true
            })
        });
        
        if (response.ok) {
            // Descargar el archivo
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `reporte_${reportType}_${fechaInicio}_${fechaFin}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('Archivo Excel descargado exitosamente', 'success');
        } else {
            showNotification('Error al generar el archivo Excel', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al exportar a Excel', 'error');
    }
}

// ====================================
// NOTIFICACIONES
// ====================================
function showNotification(message, type) {
    const notification = document.getElementById('notification');
    const icon = document.getElementById('notification-icon');
    const messageElement = document.getElementById('notification-message');
    
    const icons = {
        'success': 'fas fa-check-circle text-green-500',
        'error': 'fas fa-times-circle text-red-500',
        'warning': 'fas fa-exclamation-triangle text-yellow-500',
        'info': 'fas fa-info-circle text-blue-500'
    };
    
    icon.className = icons[type] || icons['info'];
    messageElement.textContent = message;
    
    const borderColors = {
        'success': 'border-green-500',
        'error': 'border-red-500',
        'warning': 'border-yellow-500',
        'info': 'border-blue-500'
    };
    
    notification.querySelector('div').className = `bg-white ${borderColors[type] || borderColors['info']} border-l-4 rounded-lg shadow-lg p-4 max-w-md`;
    
    notification.classList.remove('hidden');
    
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 4000);
}

