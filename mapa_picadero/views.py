from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ZonaPicadero


@login_required
def mapa_interactivo(request):
    zonas = ZonaPicadero.objects.filter(activo=True)
    libres = zonas.filter(estado='LIBRE').count()
    ocupados = zonas.filter(estado='OCUPADO').count()
    limpieza = zonas.filter(estado='LIMPIEZA').count()
    context = {
        'zonas': zonas,
        'libres': libres,
        'ocupados': ocupados,
        'limpieza': limpieza,
    }
    return render(request, 'mapa_picadero/mapa.html', context)


@login_required
def zona_detalle(request, pk):
    zona = get_object_or_404(ZonaPicadero, pk=pk)
    return render(request, 'mapa_picadero/_zona_detalle.html', {'zona': zona})
