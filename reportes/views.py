from datetime import timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from facturacion.models import Factura
from caja.models import MovimientoCaja
from caballos.models import Caballo, ControlHerraje, ControlVeterinario
from propietarios.models import Propietario
from entrenamientos.models import Entrenamiento
from inventario.models import Producto


@login_required
def reporte_mensual(request):
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    facturas = Factura.objects.filter(fecha_emision__year=year, fecha_emision__month=month)
    facturado = facturas.aggregate(total=Sum('total'))['total'] or 0
    cobrado = facturas.filter(estado='PAGADO').aggregate(total=Sum('total'))['total'] or 0
    pendiente = facturas.filter(estado='PENDIENTE').aggregate(total=Sum('total'))['total'] or 0
    
    movimientos = MovimientoCaja.objects.filter(fecha__year=year, fecha__month=month)
    ingresos = movimientos.filter(tipo='INGRESO').aggregate(total=Sum('importe'))['total'] or 0
    gastos = movimientos.filter(tipo='GASTO').aggregate(total=Sum('importe'))['total'] or 0
    
    return render(request, 'reportes/mensual.html', {
        'year': year,
        'month': month,
        'facturado': facturado,
        'cobrado': cobrado,
        'pendiente': pendiente,
        'ingresos': ingresos,
        'gastos': gastos,
        'saldo': ingresos - gastos,
        'num_facturas': facturas.count(),
        'num_caballos': Caballo.objects.count(),
        'num_propietarios': Propietario.objects.filter(activo=True).count(),
    })


@login_required
def informe_semanal(request):
    hoy = timezone.now().date()
    lunes = hoy - timedelta(days=hoy.weekday())
    domingo = lunes + timedelta(days=6)

    ingresos = MovimientoCaja.objects.filter(fecha__gte=lunes, fecha__lte=domingo, tipo='INGRESO').aggregate(total=Sum('importe'))['total'] or 0
    gastos = MovimientoCaja.objects.filter(fecha__gte=lunes, fecha__lte=domingo, tipo='GASTO').aggregate(total=Sum('importe'))['total'] or 0
    saldo = (ingresos or 0) - (gastos or 0)

    facturas = Factura.objects.filter(fecha_emision__gte=lunes, fecha_emision__lte=domingo)
    facturado = facturas.aggregate(total=Sum('total'))['total'] or 0
    cobrado = facturas.filter(estado='PAGADO').aggregate(total=Sum('total'))['total'] or 0
    pendiente = facturas.filter(estado='PENDIENTE').aggregate(total=Sum('total'))['total'] or 0

    entrenamientos = Entrenamiento.objects.filter(fecha__gte=lunes, fecha__lte=domingo)
    completados = entrenamientos.filter(completado=True).count()

    context = {
        'lunes': lunes,
        'domingo': domingo,
        'ingresos': ingresos,
        'gastos': gastos,
        'saldo': saldo,
        'facturado': facturado,
        'cobrado': cobrado,
        'pendiente': pendiente,
        'num_facturas': facturas.count(),
        'entrenamientos': entrenamientos,
        'entrenamientos_completados': completados,
        'alertas_stock': list(Producto.objects.filter(stock_actual__lte=F('stock_minimo'))),
        'herrajes': list(ControlHerraje.objects.filter(proximo_herraje__gte=hoy, proximo_herraje__lte=domingo).select_related('caballo')),
        'vacunas': list(ControlVeterinario.objects.filter(proxima_fecha__gte=hoy, proxima_fecha__lte=domingo, tipo__in=['VACUNA', 'DESPARASITACION']).select_related('caballo')),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Informe_Semanal.pdf"'
    template = get_template('reportes/informe_semanal.html')
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=400)
    return response


@login_required
def simulador(request):
    context = {
        'num_caballos': 20,
        'precio_pupilaje': 250,
        'num_entrenamientos': 40,
        'precio_entrenamiento': 60,
        'costes_fijos': 8000,
    }
    return render(request, 'reportes/simulador.html', context)
