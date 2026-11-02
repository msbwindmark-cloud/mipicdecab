from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django import forms
from .models import Consumo


@login_required
def consumo_list(request):
    query = request.GET.get('q', '')
    consumos = Consumo.objects.order_by('-id')
    if query:
        consumos = consumos.filter(
            Q(tipo__icontains=query) |
            Q(proveedor__icontains=query) |
            Q(notas__icontains=query)
        )
    paginator = Paginator(consumos, request.GET.get("per_page", 5))
    page_obj = paginator.get_page(request.GET.get('page'))
    total = consumos.aggregate(total=Sum('importe'))['total'] or 0

    if request.htmx:
        return render(request, 'consumos/_lista.html', {'page_obj': page_obj, 'query': query, 'total': total})
    return render(request, 'consumos/list.html', {'page_obj': page_obj, 'query': query, 'total': total})


class ConsumoForm(forms.ModelForm):
    class Meta:
        model = Consumo
        fields = '__all__'
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lectura_anterior': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'lectura_actual': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'importe': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.TextInput(attrs={'class': 'form-control'}),
        }


@login_required
def consumo_create(request):
    if request.method == 'POST':
        form = ConsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consumo registrado')
            return redirect('consumo_list')
    else:
        form = ConsumoForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Registrar Consumo', 'cancel_url': '/consumos/'})


@login_required
def consumo_detail(request, pk):
    consumo = get_object_or_404(Consumo, pk=pk)
    fields = [
        {'label': 'Tipo', 'value': consumo.get_tipo_display()},
        {'label': 'Fecha', 'value': consumo.fecha},
        {'label': 'Lectura Anterior', 'value': consumo.lectura_anterior},
        {'label': 'Lectura Actual', 'value': consumo.lectura_actual},
        {'label': 'Consumo', 'value': consumo.consumo},
        {'label': 'Importe', 'value': consumo.importe},
        {'label': 'Coste Por Unidad', 'value': str(consumo.coste_por_unidad)},
        {'label': 'Proveedor', 'value': consumo.proveedor or '-'},
        {'label': 'Notas', 'value': consumo.notas or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Consumo - {consumo.get_tipo_display()}",
        'fields': fields,
        'edit_url': f'/consumos/{consumo.pk}/editar/',
        'delete_url': f'/consumos/{consumo.pk}/eliminar/',
        'list_url': '/consumos/',
    })


@login_required
def consumo_update(request, pk):
    consumo = get_object_or_404(Consumo, pk=pk)
    if request.method == 'POST':
        form = ConsumoForm(request.POST, instance=consumo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consumo actualizado')
            return redirect('consumo_detail', pk=consumo.pk)
    else:
        form = ConsumoForm(instance=consumo)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Consumo', 'cancel_url': f'/consumos/{consumo.pk}/'})


@login_required
def consumo_delete(request, pk):
    consumo = get_object_or_404(Consumo, pk=pk)
    if request.method == 'POST':
        consumo.delete()
        messages.success(request, 'Consumo eliminado')
        return redirect('consumo_list')
    return render(request, 'generic/delete.html', {'object': consumo, 'cancel_url': f'/consumos/{consumo.pk}/'})
