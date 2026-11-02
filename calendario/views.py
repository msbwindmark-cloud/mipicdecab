from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from caballos.models import ControlHerraje, ControlVeterinario
from entrenamientos.models import Entrenamiento


@login_required
def calendario(request):
    return render(request, 'calendario/index.html')


@login_required
def eventos_json(request):
    eventos = []
    herrajes = ControlHerraje.objects.filter(proximo_herraje__isnull=False).select_related('caballo')
    for h in herrajes:
        eventos.append({
            'title': f'Herraje - {h.caballo.nombre}',
            'start': h.proximo_herraje.isoformat(),
            'color': '#ffc107',
            'url': f'/caballos/{h.caballo.id}/'
        })
    
    vacunas = ControlVeterinario.objects.filter(proxima_fecha__isnull=False).select_related('caballo')
    for v in vacunas:
        color = '#dc3545' if v.tipo == 'VACUNA' else '#0dcaf0'
        eventos.append({
            'title': f'{v.get_tipo_display()} - {v.caballo.nombre}',
            'start': v.proxima_fecha.isoformat(),
            'color': color,
            'url': f'/caballos/{v.caballo.id}/'
        })
    
    entrenamientos = Entrenamiento.objects.filter(completado=False).select_related('caballo')
    for e in entrenamientos:
        eventos.append({
            'title': f"Entrenamiento - {e.caballo.nombre}",
            'start': e.fecha.isoformat(),
            'color': '#20c997',
            'url': f'/entrenamientos/{e.pk}/'
        })
    
    return JsonResponse(eventos, safe=False)
