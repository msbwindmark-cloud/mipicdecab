from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import ReservaPista
from instalaciones.models import Pista
from propietarios.models import Propietario
from caballos.models import Caballo


@login_required
def reserva_list(request):
    query = request.GET.get('q', '')
    reservas = ReservaPista.objects.select_related('pista', 'propietario', 'caballo').order_by('-id')
    if query:
        reservas = reservas.filter(
            Q(pista__nombre__icontains=query) |
            Q(propietario__nombre__icontains=query) |
            Q(motivo__icontains=query) |
            Q(estado__icontains=query)
        )
    paginator = Paginator(reservas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'reservas/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'reservas/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def reserva_create(request):
    if request.method == 'POST':
        ReservaPista.objects.create(
            pista_id=request.POST.get('pista'),
            propietario_id=request.POST.get('propietario'),
            caballo_id=request.POST.get('caballo') or None,
            fecha=request.POST.get('fecha'),
            hora_inicio=request.POST.get('hora_inicio'),
            hora_fin=request.POST.get('hora_fin'),
            motivo=request.POST.get('motivo'),
            estado=request.POST.get('estado') or 'PENDIENTE',
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Reserva creada')
        return redirect('reserva_list')
    pistas = Pista.objects.all()
    propietarios = Propietario.objects.filter(activo=True)
    caballos = Caballo.objects.all()
    return render(request, 'reservas/create.html', {'pistas': pistas, 'propietarios': propietarios, 'caballos': caballos})


class ReservaPistaForm(forms.ModelForm):
    class Meta:
        model = ReservaPista
        fields = '__all__'
        widgets = {
            'pista': forms.Select(attrs={'class': 'form-control'}),
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def reserva_detail(request, pk):
    reserva = get_object_or_404(ReservaPista, pk=pk)
    fields = [
        {'label': 'Pista', 'value': reserva.pista.nombre},
        {'label': 'Propietario', 'value': reserva.propietario},
        {'label': 'Caballo', 'value': reserva.caballo.nombre if reserva.caballo else '-'},
        {'label': 'Fecha', 'value': reserva.fecha},
        {'label': 'Hora Inicio', 'value': reserva.hora_inicio},
        {'label': 'Hora Fin', 'value': reserva.hora_fin},
        {'label': 'Motivo', 'value': reserva.motivo},
        {'label': 'Estado', 'value': reserva.get_estado_display()},
        {'label': 'Notas', 'value': reserva.notas or '-'},
        {'label': 'Fecha Creacion', 'value': reserva.fecha_creacion},
        {'label': 'Duracion Horas', 'value': reserva.duracion_horas},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Reserva - {reserva.pista.nombre}",
        'fields': fields,
        'edit_url': f'/reservas/{reserva.pk}/editar/',
        'delete_url': f'/reservas/{reserva.pk}/eliminar/',
        'list_url': '/reservas/',
    })


@login_required
def reserva_update(request, pk):
    reserva = get_object_or_404(ReservaPista, pk=pk)
    if request.method == 'POST':
        form = ReservaPistaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada')
            return redirect('reserva_detail', pk=reserva.pk)
    else:
        form = ReservaPistaForm(instance=reserva)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Reserva', 'cancel_url': f'/reservas/{reserva.pk}/'})


@login_required
def reserva_delete(request, pk):
    reserva = get_object_or_404(ReservaPista, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada')
        return redirect('reserva_list')
    return render(request, 'generic/delete.html', {'object': reserva, 'cancel_url': f'/reservas/{reserva.pk}/'})
