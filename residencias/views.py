from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Residencia
from caballos.models import Caballo
from propietarios.models import Propietario
from instalaciones.models import Box


@login_required
def residencia_list(request):
    query = request.GET.get('q', '')
    residencias = Residencia.objects.select_related('caballo', 'propietario', 'box').order_by('-id')
    if query:
        residencias = residencias.filter(
            Q(caballo__nombre__icontains=query) |
            Q(propietario__nombre__icontains=query) |
            Q(tipo__icontains=query) |
            Q(estado__icontains=query)
        )
    paginator = Paginator(residencias, request.GET.get("per_page", 5))
    page_obj = paginator.get_page(request.GET.get('page'))

    if request.htmx:
        return render(request, 'residencias/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'residencias/list.html', {'page_obj': page_obj, 'query': query})


class ResidenciaForm(forms.ModelForm):
    class Meta:
        model = Residencia
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tarifa_mensual': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'box': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def residencia_create(request):
    if request.method == 'POST':
        form = ResidenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Residencia creada')
            return redirect('residencia_list')
    else:
        form = ResidenciaForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nueva Residencia/Pupilaje', 'cancel_url': '/residencias/'})


@login_required
def residencia_detail(request, pk):
    residencia = get_object_or_404(Residencia, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': residencia.caballo.nombre},
        {'label': 'Propietario', 'value': residencia.propietario},
        {'label': 'Tipo', 'value': residencia.get_tipo_display()},
        {'label': 'Fecha Inicio', 'value': residencia.fecha_inicio},
        {'label': 'Fecha Fin', 'value': residencia.fecha_fin or '-'},
        {'label': 'Tarifa Mensual', 'value': residencia.tarifa_mensual},
        {'label': 'Dias Residencia', 'value': residencia.dias_residencia},
        {'label': 'Coste Total', 'value': residencia.coste_total},
        {'label': 'Estado', 'value': residencia.get_estado_display()},
        {'label': 'Box', 'value': str(residencia.box) if residencia.box else '-'},
        {'label': 'Notas', 'value': residencia.notas or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Residencia - {residencia.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/residencias/{residencia.pk}/editar/',
        'delete_url': f'/residencias/{residencia.pk}/eliminar/',
        'list_url': '/residencias/',
    })


@login_required
def residencia_update(request, pk):
    residencia = get_object_or_404(Residencia, pk=pk)
    if request.method == 'POST':
        form = ResidenciaForm(request.POST, instance=residencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Residencia actualizada')
            return redirect('residencia_detail', pk=residencia.pk)
    else:
        form = ResidenciaForm(instance=residencia)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Residencia', 'cancel_url': f'/residencias/{residencia.pk}/'})


@login_required
def residencia_delete(request, pk):
    residencia = get_object_or_404(Residencia, pk=pk)
    if request.method == 'POST':
        residencia.delete()
        messages.success(request, 'Residencia eliminada')
        return redirect('residencia_list')
    return render(request, 'generic/delete.html', {'object': residencia, 'cancel_url': f'/residencias/{residencia.pk}/'})
