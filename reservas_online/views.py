from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ReservaOnline
from instalaciones.models import Pista
from propietarios.models import Propietario
from caballos.models import Caballo
from django import forms


class ReservaOnlineForm(forms.ModelForm):
    class Meta:
        model = ReservaOnline
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['fecha', 'hora_inicio', 'hora_fin', 'notas']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


@login_required
def reserva_online_list(request):
    from django.core.paginator import Paginator
    from django.db.models import Q
    query = request.GET.get('q', '')
    reservas = ReservaOnline.objects.select_related('pista', 'propietario', 'caballo').order_by('-id')
    if query:
        reservas = reservas.filter(
            Q(pista__nombre__icontains=query) |
            Q(propietario__nombre__icontains=query) |
            Q(tipo__icontains=query) |
            Q(estado__icontains=query)
        )
    paginator = Paginator(reservas, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'reservas_online/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'reservas_online/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def reserva_online_create(request):
    if request.method == 'POST':
        form = ReservaOnlineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva online creada')
            return redirect('reserva_online_list')
    else:
        form = ReservaOnlineForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nueva Reserva Online', 'cancel_url': '/reservas-online/'})


@login_required
def reserva_online_detail(request, pk):
    obj = get_object_or_404(ReservaOnline, pk=pk)
    fields = [
        {'label': 'Pista', 'value': obj.pista},
        {'label': 'Propietario', 'value': obj.propietario},
        {'label': 'Caballo', 'value': obj.caballo or '-'},
        {'label': 'Fecha', 'value': obj.fecha},
        {'label': 'Hora Inicio', 'value': obj.hora_inicio},
        {'label': 'Hora Fin', 'value': obj.hora_fin},
        {'label': 'Tipo', 'value': obj.get_tipo_display()},
        {'label': 'Estado', 'value': obj.get_estado_display()},
        {'label': 'Notas', 'value': obj.notas or '-'},
        {'label': 'Fecha Solicitud', 'value': obj.fecha_solicitud},
    ]
    return render(request, 'generic/detail.html', {
        'title': f'Reserva Online - {obj.pista.nombre}',
        'fields': fields,
        'edit_url': f'/reservas-online/{obj.pk}/editar/',
        'delete_url': f'/reservas-online/{obj.pk}/eliminar/',
        'list_url': '/reservas-online/',
    })


@login_required
def reserva_online_update(request, pk):
    obj = get_object_or_404(ReservaOnline, pk=pk)
    if request.method == 'POST':
        form = ReservaOnlineForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada')
            return redirect('reserva_online_detail', pk=obj.pk)
    else:
        form = ReservaOnlineForm(instance=obj)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Reserva Online', 'cancel_url': f'/reservas-online/{obj.pk}/'})


@login_required
def reserva_online_delete(request, pk):
    obj = get_object_or_404(ReservaOnline, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Reserva eliminada')
        return redirect('reserva_online_list')
    return render(request, 'generic/delete.html', {'object': obj, 'cancel_url': f'/reservas-online/{obj.pk}/'})
