from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.utils import timezone
from .models import Medicamento, Tratamiento, AdministracionMedicamento
from caballos.models import Caballo


@login_required
def medicacion_list(request):
    query = request.GET.get('q', '')
    tratamientos = Tratamiento.objects.select_related('caballo', 'medicamento').order_by('-id')
    if query:
        tratamientos = tratamientos.filter(
            Q(caballo__nombre__icontains=query) |
            Q(medicamento__nombre__icontains=query) |
            Q(motivo__icontains=query) |
            Q(veterinario__icontains=query)
        )
    paginator = Paginator(tratamientos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'medicacion/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'medicacion/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def tratamiento_create(request):
    if request.method == 'POST':
        caballo = get_object_or_404(Caballo, pk=request.POST.get('caballo'))
        medicamento = get_object_or_404(Medicamento, pk=request.POST.get('medicamento'))
        Tratamiento.objects.create(
            caballo=caballo,
            medicamento=medicamento,
            dosis=request.POST.get('dosis'),
            frecuencia=request.POST.get('frecuencia'),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin') or None,
            estado=request.POST.get('estado') or 'ACTIVO',
            motivo=request.POST.get('motivo'),
            veterinario=request.POST.get('veterinario', ''),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Tratamiento creado')
        return redirect('medicacion_list')
    caballos = Caballo.objects.all()
    medicamentos = Medicamento.objects.all()
    return render(request, 'medicacion/create.html', {'caballos': caballos, 'medicamentos': medicamentos})


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'medicamento': forms.Select(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'veterinario': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def tratamiento_update(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tratamiento actualizado')
            return redirect('tratamiento_detail', pk=tratamiento.pk)
    else:
        form = TratamientoForm(instance=tratamiento)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Tratamiento', 'cancel_url': f'/medicacion/tratamiento/{tratamiento.pk}/'})


@login_required
def tratamiento_detail(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': tratamiento.caballo.nombre},
        {'label': 'Medicamento', 'value': tratamiento.medicamento.nombre},
        {'label': 'Dosis', 'value': tratamiento.dosis},
        {'label': 'Frecuencia', 'value': tratamiento.frecuencia},
        {'label': 'Fecha Inicio', 'value': tratamiento.fecha_inicio},
        {'label': 'Fecha Fin', 'value': tratamiento.fecha_fin or '-'},
        {'label': 'Estado', 'value': tratamiento.get_estado_display()},
        {'label': 'Motivo', 'value': tratamiento.motivo},
        {'label': 'Veterinario', 'value': tratamiento.veterinario or '-'},
        {'label': 'Notas', 'value': tratamiento.notas or '-'},
        {'label': 'Activo', 'value': 'Si' if tratamiento.activo else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Tratamiento - {tratamiento.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/medicacion/tratamiento/{tratamiento.pk}/editar/',
        'delete_url': f'/medicacion/tratamiento/{tratamiento.pk}/eliminar/',
        'list_url': '/medicacion/',
    })


@login_required
def tratamiento_delete(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        tratamiento.delete()
        messages.success(request, 'Tratamiento eliminado')
        return redirect('medicacion_list')
    return render(request, 'generic/delete.html', {'object': tratamiento, 'cancel_url': f'/medicacion/tratamiento/{tratamiento.pk}/'})
