from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models
from django.db.models import Sum
from caballos.models import Caballo, ControlHerraje, ControlVeterinario
from propietarios.models import Propietario
from instalaciones.models import Box
from facturacion.models import Factura
from inventario.models import Producto
from caja.models import MovimientoCaja
from accounts.utils import get_propietario_for_user
from logros.models import LogroUsuario


@login_required
def dashboard(request):
    today = timezone.now().date()
    propietario = get_propietario_for_user(request.user)
    
    if propietario:
        total_caballos = Caballo.objects.filter(propietario=propietario).count()
        total_propietarios = 1
        facturas_pendientes = Factura.objects.filter(propietario=propietario, estado='PENDIENTE').count()
        total_boxes = Box.objects.count()
        boxes_ocupados = Box.objects.filter(estado='OCUPADO').count()
        herrajes_proximos = ControlHerraje.objects.filter(caballo__propietario=propietario, proximo_herraje__gte=today).select_related('caballo').order_by('proximo_herraje')[:10]
        vacunas_proximas = ControlVeterinario.objects.filter(caballo__propietario=propietario, proxima_fecha__gte=today, tipo__in=['VACUNA', 'DESPARASITACION']).select_related('caballo').order_by('proxima_fecha')[:10]
        productos_stock_bajo = []
        ingresos = 0
        gastos = 0
        saldo = 0
    else:
        total_caballos = Caballo.objects.count()
        total_propietarios = Propietario.objects.filter(activo=True).count()
        facturas_pendientes = Factura.objects.filter(estado='PENDIENTE').count()
        total_boxes = Box.objects.count()
        boxes_ocupados = Box.objects.filter(estado='OCUPADO').count()
        herrajes_proximos = ControlHerraje.objects.filter(proximo_herraje__gte=today).select_related('caballo').order_by('proximo_herraje')[:10]
        vacunas_proximas = ControlVeterinario.objects.filter(proxima_fecha__gte=today, tipo__in=['VACUNA', 'DESPARASITACION']).select_related('caballo').order_by('proxima_fecha')[:10]
        productos_stock_bajo = Producto.objects.filter(stock_actual__lte=models.F('stock_minimo'))
        ingresos = MovimientoCaja.objects.filter(tipo='INGRESO').aggregate(total=Sum('importe'))['total'] or 0
        gastos = MovimientoCaja.objects.filter(tipo='GASTO').aggregate(total=Sum('importe'))['total'] or 0
        saldo = ingresos - gastos
    
    context = {
        'total_caballos': total_caballos,
        'total_propietarios': total_propietarios,
        'facturas_pendientes': facturas_pendientes,
        'total_boxes': total_boxes,
        'boxes_ocupados': boxes_ocupados,
        'herrajes_proximos': herrajes_proximos,
        'vacunas_proximas': vacunas_proximas,
        'productos_stock_bajo': productos_stock_bajo,
        'ingresos': ingresos,
        'gastos': gastos,
        'saldo': saldo,
        'logros_conquistados': LogroUsuario.objects.filter(usuario=request.user).select_related('logro').order_by('-fecha')[:10],
    }
    return render(request, 'dashboard.html', context)


def landing(request):
    total_caballos = Caballo.objects.count()
    total_propietarios = Propietario.objects.filter(activo=True).count()
    facturas_pendientes = Factura.objects.filter(estado='PENDIENTE').count()
    ingresos = MovimientoCaja.objects.filter(tipo='INGRESO').aggregate(total=Sum('importe'))['total'] or 0
    return render(request, 'landing/index.html', {
        'total_caballos': total_caballos,
        'total_propietarios': total_propietarios,
        'facturas_pendientes': facturas_pendientes,
        'ingresos': ingresos,
    })