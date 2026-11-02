from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from caballos.models import Caballo
from .models import RegistroFisico


@login_required
def seguimiento_list(request, caballo_id):
    caballo = get_object_or_404(Caballo, pk=caballo_id)
    registros = caballo.registros_fisicos.all()

    pesos = [float(r.peso_kg) for r in registros.order_by('fecha')]
    fechas = [r.fecha.strftime('%d/%m/%Y') for r in registros.order_by('fecha')]
    cc = [r.condicion_corporal for r in registros.order_by('fecha')]
    musculo = [r.tono_muscular for r in registros.order_by('fecha')]

    ultimo = registros.first()
    primero = registros.last() if registros.count() > 1 else None
    evolucion = round(float(ultimo.peso_kg) - float(primero.peso_kg), 2) if ultimo and primero else 0

    context = {
        'caballo': caballo,
        'registros': registros,
        'pesos': pesos,
        'fechas': fechas,
        'cc': cc,
        'musculo': musculo,
        'ultimo': ultimo,
        'evolucion': evolucion,
    }
    return render(request, 'seguimiento_fisico/list.html', context)


@login_required
def seguimiento_create(request, caballo_id):
    caballo = get_object_or_404(Caballo, pk=caballo_id)
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        peso_kg = request.POST.get('peso_kg')
        condicion_corporal = request.POST.get('condicion_corporal')
        tono_muscular = request.POST.get('tono_muscular')
        estado = request.POST.get('estado')
        observaciones = request.POST.get('observaciones', '')
        foto = request.POST.get('foto', '')

        RegistroFisico.objects.create(
            caballo=caballo,
            fecha=fecha,
            peso_kg=peso_kg,
            condicion_corporal=condicion_corporal,
            tono_muscular=tono_muscular,
            estado=estado,
            observaciones=observaciones,
            foto=foto or None,
        )
        messages.success(request, f'¡Registro físico de {caballo.nombre} guardado con éxito! La evolución empieza hoy 💪')
        return redirect('seguimiento_list', caballo_id=caballo.pk)

    return render(request, 'seguimiento_fisico/create.html', {'caballo': caballo})


@login_required
def seguimiento_delete(request, pk):
    registro = get_object_or_404(RegistroFisico, pk=pk)
    caballo_id = registro.caballo.pk
    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Registro físico eliminado correctamente.')
        return redirect('seguimiento_list', caballo_id=caballo_id)
    return redirect('seguimiento_list', caballo_id=caballo_id)
