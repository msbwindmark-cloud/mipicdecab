from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import FacturaRecurrente
from propietarios.models import Propietario


@login_required
def recurrente_list(request):
    query = request.GET.get('q', '')
    recurrentes = FacturaRecurrente.objects.select_related('propietario').order_by('-id')
    if query:
        recurrentes = recurrentes.filter(
            Q(propietario__nombre__icontains=query) |
            Q(concepto__icontains=query) |
            Q(frecuencia__icontains=query)
        )
    paginator = Paginator(recurrentes, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'facturacion_recurrente/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'facturacion_recurrente/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def recurrente_create(request):
    if request.method == 'POST':
        FacturaRecurrente.objects.create(
            propietario_id=request.POST.get('propietario'),
            concepto=request.POST.get('concepto'),
            importe=request.POST.get('importe'),
            frecuencia=request.POST.get('frecuencia'),
            dia_emision=request.POST.get('dia_emision', 1),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin') or None,
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Factura recurrente creada')
        return redirect('recurrente_list')
    propietarios = Propietario.objects.filter(activo=True)
    return render(request, 'facturacion_recurrente/create.html', {'propietarios': propietarios})


class FacturaRecurrenteForm(forms.ModelForm):
    class Meta:
        model = FacturaRecurrente
        fields = '__all__'
        widgets = {
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'importe': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'frecuencia': forms.Select(attrs={'class': 'form-control'}),
            'dia_emision': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def recurrente_detail(request, pk):
    recurrente = get_object_or_404(FacturaRecurrente, pk=pk)
    fields = [
        {'label': 'Propietario', 'value': recurrente.propietario.nombre},
        {'label': 'Concepto', 'value': recurrente.concepto},
        {'label': 'Importe', 'value': recurrente.importe},
        {'label': 'Frecuencia', 'value': recurrente.get_frecuencia_display()},
        {'label': 'Dia Emision', 'value': recurrente.dia_emision},
        {'label': 'Fecha Inicio', 'value': recurrente.fecha_inicio},
        {'label': 'Fecha Fin', 'value': recurrente.fecha_fin or '-'},
        {'label': 'Activa', 'value': 'Si' if recurrente.activa else 'No'},
        {'label': 'Ultima Emision', 'value': recurrente.ultima_emision or '-'},
        {'label': 'Notas', 'value': recurrente.notas or '-'},
        {'label': 'Proxima Emision', 'value': recurrente.proxima_emision},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Factura Recurrente - {recurrente.concepto}",
        'fields': fields,
        'edit_url': f'/facturacion-recurrente/{recurrente.pk}/editar/',
        'delete_url': f'/facturacion-recurrente/{recurrente.pk}/eliminar/',
        'list_url': '/facturacion-recurrente/',
    })


@login_required
def recurrente_update(request, pk):
    recurrente = get_object_or_404(FacturaRecurrente, pk=pk)
    if request.method == 'POST':
        form = FacturaRecurrenteForm(request.POST, instance=recurrente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Factura recurrente actualizada')
            return redirect('recurrente_detail', pk=recurrente.pk)
    else:
        form = FacturaRecurrenteForm(instance=recurrente)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Factura Recurrente', 'cancel_url': f'/facturacion-recurrente/{recurrente.pk}/'})


@login_required
def recurrente_delete(request, pk):
    recurrente = get_object_or_404(FacturaRecurrente, pk=pk)
    if request.method == 'POST':
        recurrente.delete()
        messages.success(request, 'Factura recurrente eliminada')
        return redirect('recurrente_list')
    return render(request, 'generic/delete.html', {'object': recurrente, 'cancel_url': f'/facturacion-recurrente/{recurrente.pk}/'})
