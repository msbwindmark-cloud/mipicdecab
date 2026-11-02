from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from caballos.models import Caballo
from caballos.models import ControlVeterinario, ControlHerraje
from entrenamientos.models import Entrenamiento
from seguimiento_fisico.models import RegistroFisico


@login_required
def timeline_caballo(request, caballo_id):
    caballo = get_object_or_404(Caballo, pk=caballo_id)
    eventos = []

    for v in ControlVeterinario.objects.filter(caballo=caballo):
        eventos.append({'fecha': v.fecha_realizada, 'tipo': 'VETERINARIO', 'titulo': v.get_tipo_display(), 'detalle': v.descripcion or '', 'icono': 'fa-syringe', 'color': 'danger'})

    for h in ControlHerraje.objects.filter(caballo=caballo):
        eventos.append({'fecha': h.fecha, 'tipo': 'HERRAJE', 'titulo': 'Herraje', 'detalle': h.herrador or '', 'icono': 'fa-hammer', 'color': 'warning'})

    for e in Entrenamiento.objects.filter(caballo=caballo):
        eventos.append({'fecha': e.fecha, 'tipo': 'ENTRENAMIENTO', 'titulo': e.get_tipo_display(), 'detalle': e.observaciones or '', 'icono': 'fa-running', 'color': 'success'})

    for f in RegistroFisico.objects.filter(caballo=caballo):
        eventos.append({'fecha': f.fecha, 'tipo': 'FISICO', 'titulo': 'Seguimiento Físico', 'detalle': f'Peso: {f.peso_kg}kg | CC: {f.condicion_corporal}/5 | TM: {f.tono_muscular}/5', 'icono': 'fa-chart-line', 'color': 'primary'})

    eventos.sort(key=lambda x: x['fecha'], reverse=True)
    context = {'caballo': caballo, 'eventos': eventos}
    return render(request, 'timeline_caballo/timeline.html', context)
