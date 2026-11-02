from .models import ConfiguracionPicadero
from django.utils import timezone
from caballos.models import ControlHerraje, ControlVeterinario
from inventario.models import Producto
from facturacion.models import Factura
from django.db import models


def config_picadero(request):
    try:
        config = ConfiguracionPicadero.objects.first()
    except:
        config = None
    return {'config_picadero': config}


def alertas(request):
    if not request.user.is_authenticated:
        return {'alertas_count': 0, 'alertas_list': []}
    
    today = timezone.now().date()
    alertas = []
    
    # Herrajes vencidos/próximos
    herrajes = ControlHerraje.objects.filter(proximo_herraje__lte=today + timezone.timedelta(days=7)).select_related('caballo')[:5]
    for h in herrajes:
        alertas.append({'tipo': 'herraje', 'texto': f'Herraje próximo: {h.caballo.nombre}', 'url': f'/caballos/{h.caballo.pk}/'})
    
    # Vacunas próximas
    vacunas = ControlVeterinario.objects.filter(proxima_fecha__lte=today + timezone.timedelta(days=7), tipo__in=['VACUNA', 'DESPARASITACION']).select_related('caballo')[:5]
    for v in vacunas:
        alertas.append({'tipo': 'vacuna', 'texto': f'{v.get_tipo_display()} próxima: {v.caballo.nombre}', 'url': f'/caballos/{v.caballo.pk}/'})
    
    # Stock bajo
    stock_bajo = Producto.objects.filter(stock_actual__lte=models.F('stock_minimo'))[:5]
    for p in stock_bajo:
        alertas.append({'tipo': 'stock', 'texto': f'Stock bajo: {p.nombre}', 'url': '/inventario/'})
    
    # Facturas vencidas
    facturas_vencidas = Factura.objects.filter(estado='PENDIENTE', fecha_vencimiento__lt=today)[:5]
    for f in facturas_vencidas:
        alertas.append({'tipo': 'factura', 'texto': f'Factura vencida: {f.numero_factura}', 'url': f'/facturacion/{f.pk}/'})
    
    return {'alertas_count': len(alertas), 'alertas_list': alertas[:10]}