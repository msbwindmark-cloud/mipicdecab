from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Box, Pista


@login_required
def instalaciones(request):
    boxes = Box.objects.all().order_by('numero')
    pistas = Pista.objects.all()
    return render(request, 'instalaciones/index.html', {'boxes': boxes, 'pistas': pistas})


@login_required
def mapa_boxes(request):
    boxes = Box.objects.all().order_by('bloque', 'numero')
    return render(request, 'instalaciones/mapa_boxes.html', {'boxes': boxes})
