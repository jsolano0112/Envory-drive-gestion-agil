# views/driver_history_views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg, Count
from datetime import datetime, date
import csv
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfgen import canvas

from .models import Conductor, Vehiculo


@login_required
def driver_history(request):
    """Vista principal del historial de conductor"""
    context = {
        'driver': None,
        'search_term': '',
        'active_tab': 'viajes',
        'date_start': '',
        'date_end': ''
    }
    
    search_term = request.GET.get('search', '')
    active_tab = request.GET.get('tab', 'viajes')
    date_start = request.GET.get('date_start', '')
    date_end = request.GET.get('date_end', '')
    
    if search_term:
        # Buscar conductor por nombre, documento o placa
        driver = Conductor.objects.filter(
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term) |
            Q(numero_documento__icontains=search_term) |
            Q(vehiculo__placa__icontains=search_term)
        ).select_related('user', 'vehiculo').first()
        
        if driver:
            # TODO: Cuando tengas el modelo de Viajes (Trip), reemplaza esto:
            # Calcular estadísticas reales
            # trips_queryset = Trip.objects.filter(conductor=driver)
            
            # Por ahora, datos de ejemplo:
            stats = {
                'total_trips': 247,
                'avg_rating': 4.8,
                'completion_rate': 96,
                'total_reports': 2
            }
            
            # TODO: Filtrar viajes por fecha cuando implementes el modelo Trip
            # if date_start and date_end:
            #     trips_queryset = trips_queryset.filter(
            #         fecha__range=[date_start, date_end]
            #     )
            
            # TODO: Obtener viajes reales
            # trips = trips_queryset.select_related('cliente').order_by('-fecha')[:20]
            trips = []  # Placeholder
            
            # TODO: Obtener historial de estados real cuando implementes el modelo
            # status_history = StatusHistory.objects.filter(
            #     conductor=driver
            # ).order_by('-fecha')[:20]
            status_history = []  # Placeholder
            
            context.update({
                'driver': driver,
                'stats': stats,
                'trips': trips,
                'status_history': status_history,
                'search_term': search_term,
                'active_tab': active_tab,
                'date_start': date_start,
                'date_end': date_end
            })
    
    return render(request, 'driver_details.html', context)



@csrf_exempt
@require_http_methods(["POST"])
def update_driver_status(request, driver_id):
    """
    Actualiza el estado del conductor y registra el cambio en el historial.
    """
    try:
        driver = get_object_or_404(Conductor, id=driver_id)
        new_status = request.POST.get('status')
        
        # Validar estado
        valid_statuses = ['Activo', 'Inactivo', 'Suspendido', 'Bloqueado', 'En Revisión']
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'message': 'Estado no válido'
            }, status=400)
        
        # Guardar estado anterior
        old_status = driver.estado
        
        # Actualizar estado del conductor
        driver.estado = new_status
        driver.save()
        
        # TODO: Crear registro en historial de cambios de estado
        # StatusHistory.objects.create(
        #     conductor=driver,
        #     previous_status=old_status,
        #     new_status=new_status,
        #     reason=request.POST.get('reason', 'Cambio manual'),
        #     modified_by=request.user
        # )
        
        # Redirigir de vuelta al historial con el mismo conductor
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}?search={driver.numero_documento}")
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al actualizar estado: {str(e)}'
        }, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def generate_report(request, driver_id):
    """
    Genera reportes en PDF según el tipo seleccionado:
    - monthly: Reporte de viajes por mes
    - daily: Reporte de viajes por día
    - monetary: Reporte monetario
    """
    try:
        driver = get_object_or_404(Conductor, id=driver_id)
        report_type = request.POST.get('report_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Validar campos requeridos
        if not report_type or not start_date or not end_date:
            return JsonResponse({
                'success': False,
                'message': 'Faltan campos requeridos'
            }, status=400)
        
        # Convertir fechas
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Validar que la fecha de inicio sea anterior a la fecha final
        if start_date_obj > end_date_obj:
            return JsonResponse({
                'success': False,
                'message': 'La fecha de inicio debe ser anterior a la fecha final'
            }, status=400)
        
        # TODO: Cuando tengas el modelo de viajes, filtra los datos reales
        # trips = Trip.objects.filter(
        #     conductor=driver,
        #     fecha__range=[start_date_obj, end_date_obj]
        # )
        
        # Crear el PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para el título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1E40AF'),
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        # Título del reporte
        report_titles = {
            'monthly': 'Reporte de Viajes por Mes',
            'daily': 'Reporte de Viajes por Día',
            'monetary': 'Reporte Monetario'
        }
        title = Paragraph(report_titles.get(report_type, 'Reporte'), title_style)
        elements.append(title)
        
        # Información del conductor
        info_data = [
            ['Conductor:', driver.get_nombre_completo()],
            ['Documento:', driver.numero_documento],
            ['Placa:', driver.vehiculo.placa if hasattr(driver, 'vehiculo') else 'N/A'],
            ['Período:', f'{start_date} al {end_date}'],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E5E7EB')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # TODO: Agregar datos reales del reporte según el tipo
        if report_type == 'monthly':
            # Reporte por mes
            elements.append(Paragraph('Resumen Mensual', styles['Heading2']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Datos de ejemplo (reemplazar con datos reales)
            data = [
                ['Mes', 'Viajes', 'Ingresos'],
                ['Octubre 2025', '85', '$2,850,000'],
                ['Septiembre 2025', '78', '$2,640,000'],
                ['Agosto 2025', '84', '$2,856,000'],
            ]
            
        elif report_type == 'daily':
            # Reporte por día
            elements.append(Paragraph('Resumen Diario', styles['Heading2']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Datos de ejemplo
            data = [
                ['Fecha', 'Viajes', 'Horas Trabajadas', 'Ingresos'],
                ['26 Oct 2025', '12', '8.5', '$420,000'],
                ['25 Oct 2025', '10', '7.2', '$350,000'],
                ['24 Oct 2025', '15', '9.8', '$525,000'],
            ]
            
        elif report_type == 'monetary':
            # Reporte monetario
            elements.append(Paragraph('Resumen Financiero', styles['Heading2']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Datos de ejemplo
            data = [
                ['Concepto', 'Monto'],
                ['Total Ingresos', '$2,850,000'],
                ['Comisión Plataforma (20%)', '$570,000'],
                ['Neto a Pagar', '$2,280,000'],
                ['Viajes Realizados', '247'],
                ['Promedio por Viaje', '$11,538'],
            ]
        
        # Crear tabla con los datos
        if data:
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        
        # Generar el PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Preparar la respuesta
        response = HttpResponse(buffer, content_type='application/pdf')
        filename = f'reporte_{report_type}_{driver.numero_documento}_{start_date}_{end_date}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al generar reporte: {str(e)}'
        }, status=500)



def export_history(request, driver_id):
    """
    Exporta el historial completo del conductor a CSV.
    Incluye: información personal, vehículo, estadísticas y viajes.
    """
    try:
        driver = get_object_or_404(Conductor, id=driver_id)
        
        # Crear respuesta CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="historial_{driver.numero_documento}.csv"'
        
        # Agregar BOM para Excel
        response.write('\ufeff')
        
        writer = csv.writer(response)
        
        # Escribir información del conductor
        writer.writerow(['INFORMACIÓN DEL CONDUCTOR'])
        writer.writerow(['Nombre Completo', driver.get_nombre_completo()])
        writer.writerow(['Documento', driver.numero_documento])
        writer.writerow(['Email', driver.user.email])
        writer.writerow(['Teléfono', driver.telefono_principal])
        writer.writerow(['Ciudad', driver.ciudad])
        writer.writerow(['Estado', driver.estado])
        writer.writerow(['Fecha Registro', driver.fecha_registro.strftime('%Y-%m-%d')])
        writer.writerow([])  # Línea vacía
        
        # Información del vehículo
        if hasattr(driver, 'vehiculo'):
            writer.writerow(['INFORMACIÓN DEL VEHÍCULO'])
            writer.writerow(['Placa', driver.vehiculo.placa])
            writer.writerow(['Marca', driver.vehiculo.marca])
            writer.writerow(['Modelo', driver.vehiculo.modelo])
            writer.writerow(['Año', driver.vehiculo.anio])
            writer.writerow(['Color', driver.vehiculo.color])
            writer.writerow(['Tipo', driver.vehiculo.tipo_vehiculo])
            writer.writerow([])
        
        # Estadísticas
        writer.writerow(['ESTADÍSTICAS'])
        writer.writerow(['Total Viajes', '247'])  # TODO: Reemplazar con datos reales
        writer.writerow(['Calificación Promedio', '4.8'])
        writer.writerow(['Tasa Completado', '96%'])
        writer.writerow(['Reportes', '2'])
        writer.writerow([])
        
        # TODO: Agregar historial de viajes cuando implementes el modelo
        # writer.writerow(['HISTORIAL DE VIAJES'])
        # writer.writerow(['Fecha', 'Origen', 'Destino', 'Cliente', 'Estado', 'Calificación', 'Monto'])
        # 
        # trips = Trip.objects.filter(conductor=driver).order_by('-fecha')
        # for trip in trips:
        #     writer.writerow([
        #         trip.fecha.strftime('%Y-%m-%d %H:%M'),
        #         trip.origen,
        #         trip.destino,
        #         trip.cliente.get_nombre_completo(),
        #         trip.estado,
        #         trip.calificacion or 'N/A',
        #         f'${trip.monto:,.0f}'
        #     ])
        
        return response
    
    except Exception as e:
        return HttpResponse(f'Error al exportar: {str(e)}', status=500)



@require_http_methods(["GET"])
def driver_statistics_api(request, driver_id):
    """
    Endpoint API para obtener estadísticas del conductor en formato JSON.
    Útil para dashboards o consultas programáticas.
    """
    try:
        driver = get_object_or_404(Conductor, id=driver_id)
        
        # TODO: Calcular con datos reales cuando tengas el modelo Trip
        # trips = Trip.objects.filter(conductor=driver)
        # total_trips = trips.count()
        # completed_trips = trips.filter(estado='Completado').count()
        # avg_rating = trips.filter(calificacion__isnull=False).aggregate(Avg('calificacion'))['calificacion__avg']
        
        statistics = {
            'conductor': {
                'id': driver.id,
                'nombre_completo': driver.get_nombre_completo(),
                'numero_documento': driver.numero_documento,
                'email': driver.user.email,
                'estado': driver.estado,
                'fecha_registro': driver.fecha_registro.strftime('%Y-%m-%d')
            },
            'vehiculo': {
                'placa': driver.vehiculo.placa if hasattr(driver, 'vehiculo') else None,
                'marca': driver.vehiculo.marca if hasattr(driver, 'vehiculo') else None,
                'modelo': driver.vehiculo.modelo if hasattr(driver, 'vehiculo') else None,
            } if hasattr(driver, 'vehiculo') else None,
            'stats': {
                'total_viajes': 247,  # Placeholder
                'calificacion_promedio': 4.8,
                'tasa_completado': 96,
                'total_reportes': 2,
                'viajes_mes_actual': 28,
                'ingresos_totales': 8950000
            }
        }
        
        return JsonResponse({
            'success': True,
            'data': statistics
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }, status=500)