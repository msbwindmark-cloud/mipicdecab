from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Mantenimiento
from instalaciones.models import Box, Pista


@login_required
def mantenimiento_list(request):
    query = request.GET.get('q', '')
    mantenimientos = Mantenimiento.objects.select_related('box', 'pista').order_by('-id')
    if query:
        mantenimientos = mantenimientos.filter(
            Q(descripcion__icontains=query) |
            Q(tipo__icontains=query) |
            Q(realizado_por__icontains=query) |
            Q(box__numero__icontains=query)
        )
    paginator = Paginator(mantenimientos, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'mantenimiento/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'mantenimiento/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def mantenimiento_create(request):
    if request.method == 'POST':
        Mantenimiento.objects.create(
            instalacion_tipo=request.POST.get('instalacion_tipo'),
            box_id=request.POST.get('box') or None,
            pista_id=request.POST.get('pista') or None,
            tipo=request.POST.get('tipo'),
            descripcion=request.POST.get('descripcion'),
            fecha_inicio=request.POST.get('fecha_inicio') or None,
            coste=request.POST.get('coste', 0),
            realizado_por=request.POST.get('realizado_por', ''),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Mantenimiento registrado')
        return redirect('mantenimiento_list')
    boxes = Box.objects.all()
    pistas = Pista.objects.all()
    return render(request, 'mantenimiento/create.html', {'boxes': boxes, 'pistas': pistas})


class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = '__all__'
        widgets = {
            'instalacion_tipo': forms.Select(attrs={'class': 'form-control'}),
            'box': forms.Select(attrs={'class': 'form-control'}),
            'pista': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'coste': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'realizado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def mantenimiento_detail(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    fields = [
        {'label': 'Instalacion', 'value': f"Box {mantenimiento.box.numero}" if mantenimiento.box else (f"Pista {mantenimiento.pista.nombre}" if mantenimiento.pista else '-')},
        {'label': 'Tipo', 'value': mantenimiento.get_tipo_display()},
        {'label': 'Descripcion', 'value': mantenimiento.descripcion},
        {'label': 'Fecha Reporte', 'value': mantenimiento.fecha_reporte},
        {'label': 'Fecha Inicio', 'value': mantenimiento.fecha_inicio or '-'},
        {'label': 'Fecha Fin', 'value': mantenimiento.fecha_fin or '-'},
        {'label': 'Coste', 'value': mantenimiento.coste},
        {'label': 'Realizado Por', 'value': mantenimiento.realizado_por or '-'},
        {'label': 'Estado', 'value': mantenimiento.get_estado_display()},
        {'label': 'Notas', 'value': mantenimiento.notas or '-'},
        {'label': 'Vencido', 'value': 'Si' if mantenimiento.vencido else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Mantenimiento - {mantenimiento.get_tipo_display()}",
        'fields': fields,
        'edit_url': f'/mantenimiento/{mantenimiento.pk}/editar/',
        'delete_url': f'/mantenimiento/{mantenimiento.pk}/eliminar/',
        'list_url': '/mantenimiento/',
    })


@login_required
def mantenimiento_update(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mantenimiento actualizado')
            return redirect('mantenimiento_detail', pk=mantenimiento.pk)
    else:
        form = MantenimientoForm(instance=mantenimiento)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Mantenimiento', 'cancel_url': f'/mantenimiento/{mantenimiento.pk}/'})


@login_required
def mantenimiento_delete(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        mantenimiento.delete()
        messages.success(request, 'Mantenimiento eliminado')
        return redirect('mantenimiento_list')
    return render(request, 'generic/delete.html', {'object': mantenimiento, 'cancel_url': f'/mantenimiento/{mantenimiento.pk}/'})
