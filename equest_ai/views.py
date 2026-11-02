from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import F
from caballos.models import Caballo, ControlHerraje, ControlVeterinario
from facturacion.models import Factura
from inventario.models import Producto
import json
from datetime import timedelta


@login_required
def equest_ai_home(request):
    return render(request, 'equest_ai/assistant.html', {})


@login_required
def equest_ai_responder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hoy = timezone.now().date()
            facturas = Factura.objects.filter(estado='PENDIENTE').count()
            herrajes = ControlHerraje.objects.filter(proximo_herraje__gte=hoy, proximo_herraje__lte=hoy + timedelta(days=30)).count()
            vacunas = ControlVeterinario.objects.filter(proxima_fecha__gte=hoy, proxima_fecha__lte=hoy + timedelta(days=30)).count()
            stock_bajo = Producto.objects.filter(stock_actual__lte=F('stock_minimo')).count()
            respuesta = f'Facturas pendientes: {facturas}. Herrajes próximos 30 días: {herrajes}. Vacunas/Desparasitaciones próximos 30 días: {vacunas}. Stock bajo: {stock_bajo}.'
            return JsonResponse({'respuesta': respuesta, 'sugerencias': ['Ver facturas pendientes', 'Ver herrajes próximos', 'Ver stock bajo']})
        except Exception as e:
            return JsonResponse({'respuesta': f'Error: {e}'}, status=500)
    return JsonResponse({'respuesta': 'POST requerida'}, status=400)
