from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Reproduccion, ControlGestacion
from caballos.models import Caballo
from propietarios.models import Propietario


@login_required
def reproduccion_list(request):
    query = request.GET.get('q', '')
    reproducciones = Reproduccion.objects.select_related('yegua', 'semental', 'potro').order_by('-id')
    if query:
        reproducciones = reproducciones.filter(
            Q(yegua__nombre__icontains=query) |
            Q(semental__nombre__icontains=query) |
            Q(tipo__icontains=query) |
            Q(estado__icontains=query)
        )
    paginator = Paginator(reproducciones, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'reproduccion/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'reproduccion/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def reproduccion_create(request):
    if request.method == 'POST':
        Reproduccion.objects.create(
            yegua_id=request.POST.get('yegua'),
            semental_id=request.POST.get('semental') or None,
            tipo=request.POST.get('tipo'),
            fecha_cubricion=request.POST.get('fecha_cubricion'),
            fecha_parto_estimada=request.POST.get('fecha_parto_estimada') or None,
            fecha_parto_real=request.POST.get('fecha_parto_real') or None,
            estado=request.POST.get('estado') or 'CUBRICION',
            potro_id=request.POST.get('poto') or None,
            veterinario=request.POST.get('veterinario', ''),
            coste=request.POST.get('coste', 0),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Reproducción registrada')
        return redirect('reproduccion_list')
    caballos = Caballo.objects.all()
    return render(request, 'reproduccion/create.html', {'caballos': caballos})


class ReproduccionForm(forms.ModelForm):
    class Meta:
        model = Reproduccion
        fields = '__all__'
        widgets = {
            'yegua': forms.Select(attrs={'class': 'form-control'}),
            'semental': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_cubricion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_parto_estimada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_parto_real': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'poto': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.TextInput(attrs={'class': 'form-control'}),
            'coste': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def reproduccion_detail(request, pk):
    reproduccion = get_object_or_404(Reproduccion, pk=pk)
    fields = [
        {'label': 'Yegua', 'value': reproduccion.yegua.nombre},
        {'label': 'Semental', 'value': reproduccion.semental.nombre if reproduccion.semental else '-'},
        {'label': 'Tipo', 'value': reproduccion.get_tipo_display()},
        {'label': 'Fecha Cubricion', 'value': reproduccion.fecha_cubricion},
        {'label': 'Parto Estimada', 'value': reproduccion.fecha_parto_estimada or '-'},
        {'label': 'Parto Real', 'value': reproduccion.fecha_parto_real or '-'},
        {'label': 'Estado', 'value': reproduccion.get_estado_display()},
        {'label': 'Poto', 'value': reproduccion.poto.nombre if reproduccion.poto else '-'},
        {'label': 'Veterinario', 'value': reproduccion.veterinario or '-'},
        {'label': 'Coste', 'value': reproduccion.coste},
        {'label': 'Notas', 'value': reproduccion.notas or '-'},
        {'label': 'Dias Gestacion', 'value': reproduccion.dias_gestacion},
        {'label': 'Gestacion Completada', 'value': 'Si' if reproduccion.gestacion_completada else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Reproducción - {reproduccion.yegua.nombre}",
        'fields': fields,
        'edit_url': f'/reproduccion/{reproduccion.pk}/editar/',
        'delete_url': f'/reproduccion/{reproduccion.pk}/eliminar/',
        'list_url': '/reproduccion/',
    })


@login_required
def reproduccion_update(request, pk):
    reproduccion = get_object_or_404(Reproduccion, pk=pk)
    if request.method == 'POST':
        form = ReproduccionForm(request.POST, instance=reproduccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reproducción actualizada')
            return redirect('reproduccion_detail', pk=reproduccion.pk)
    else:
        form = ReproduccionForm(instance=reproduccion)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Reproducción', 'cancel_url': f'/reproduccion/{reproduccion.pk}/'})


@login_required
def reproduccion_delete(request, pk):
    reproduccion = get_object_or_404(Reproduccion, pk=pk)
    if request.method == 'POST':
        reproduccion.delete()
        messages.success(request, 'Reproducción eliminada')
        return redirect('reproduccion_list')
    return render(request, 'generic/delete.html', {'object': reproduccion, 'cancel_url': f'/reproduccion/{reproduccion.pk}/'})


class ControlGestacionForm(forms.ModelForm):
    class Meta:
        model = ControlGestacion
        fields = '__all__'
        widgets = {
            'reproduccion': forms.Select(attrs={'class': 'form-control'}),
            'semana_gestacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'peso_yegua': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'veterinario': forms.TextInput(attrs={'class': 'form-control'}),
        }


@login_required
def control_create(request):
    if request.method == 'POST':
        form = ControlGestacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Control de gestación registrado')
            return redirect('reproduccion_list')
    else:
        form = ControlGestacionForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nuevo Control de Gestación', 'cancel_url': '/reproduccion/'})


@login_required
def control_detail(request, pk):
    control = get_object_or_404(ControlGestacion, pk=pk)
    fields = [
        {'label': 'Reproduccion', 'value': control.reproduccion.yegua.nombre},
        {'label': 'Fecha', 'value': control.fecha},
        {'label': 'Semana Gestacion', 'value': control.semana_gestacion},
        {'label': 'Observaciones', 'value': control.observaciones},
        {'label': 'Peso Yegua', 'value': control.peso_yegua or '-'},
        {'label': 'Veterinario', 'value': control.veterinario or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Control Gestación - {control.reproduccion.yegua.nombre}",
        'fields': fields,
        'edit_url': f'/reproduccion/control/{control.pk}/editar/',
        'delete_url': f'/reproduccion/control/{control.pk}/eliminar/',
        'list_url': '/reproduccion/',
    })


@login_required
def control_update(request, pk):
    control = get_object_or_404(ControlGestacion, pk=pk)
    if request.method == 'POST':
        form = ControlGestacionForm(request.POST, instance=control)
        if form.is_valid():
            form.save()
            messages.success(request, 'Control de gestación actualizado')
            return redirect('control_detail', pk=control.pk)
    else:
        form = ControlGestacionForm(instance=control)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Control de Gestación', 'cancel_url': f'/reproduccion/control/{control.pk}/'})


@login_required
def control_delete(request, pk):
    control = get_object_or_404(ControlGestacion, pk=pk)
    if request.method == 'POST':
        control.delete()
        messages.success(request, 'Control de gestación eliminado')
        return redirect('reproduccion_list')
    return render(request, 'generic/delete.html', {'object': control, 'cancel_url': f'/reproduccion/control/{control.pk}/'})
