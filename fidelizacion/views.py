from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import PuntosFidelizacion, MovimientoPuntos, Recompensa
from propietarios.models import Propietario


@login_required
def fidelizacion_list(request):
    query = request.GET.get('q', '')
    puntos = PuntosFidelizacion.objects.select_related('propietario').order_by('-id')
    if query:
        puntos = puntos.filter(
            Q(propietario__nombre__icontains=query) |
            Q(propietario__apellidos__icontains=query)
        )
    paginator = Paginator(puntos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    recompensas = Recompensa.objects.filter(activa=True)
    
    if request.htmx:
        return render(request, 'fidelizacion/_lista.html', {'page_obj': page_obj, 'query': query, 'recompensas': recompensas})
    return render(request, 'fidelizacion/list.html', {'page_obj': page_obj, 'query': query, 'recompensas': recompensas})


class RecompensaForm(forms.ModelForm):
    class Meta:
        model = Recompensa
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'puntos_necesarios': forms.NumberInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def recompensa_list(request):
    recompensas = Recompensa.objects.order_by('-id')
    paginator = Paginator(recompensas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'fidelizacion/recompensas.html', {'page_obj': page_obj, 'recompensas': recompensas})


@login_required
def recompensa_create(request):
    if request.method == 'POST':
        form = RecompensaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recompensa creada')
            return redirect('recompensa_list')
    else:
        form = RecompensaForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nueva Recompensa', 'cancel_url': '/fidelizacion/'})


@login_required
def recompensa_detail(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    fields = [
        {'label': 'Nombre', 'value': recompensa.nombre},
        {'label': 'Descripcion', 'value': recompensa.descripcion},
        {'label': 'Puntos Necesarios', 'value': recompensa.puntos_necesarios},
        {'label': 'Activa', 'value': 'Si' if recompensa.activa else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Recompensa - {recompensa.nombre}",
        'fields': fields,
        'edit_url': f'/fidelizacion/recompensa/{recompensa.pk}/editar/',
        'delete_url': f'/fidelizacion/recompensa/{recompensa.pk}/eliminar/',
        'list_url': '/fidelizacion/',
    })


@login_required
def recompensa_update(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    if request.method == 'POST':
        form = RecompensaForm(request.POST, instance=recompensa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recompensa actualizada')
            return redirect('recompensa_detail', pk=recompensa.pk)
    else:
        form = RecompensaForm(instance=recompensa)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Recompensa', 'cancel_url': f'/fidelizacion/recompensa/{recompensa.pk}/'})


@login_required
def recompensa_delete(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    if request.method == 'POST':
        recompensa.delete()
        messages.success(request, 'Recompensa eliminada')
        return redirect('fidelizacion_list')
    return render(request, 'generic/delete.html', {'object': recompensa, 'cancel_url': f'/fidelizacion/recompensa/{recompensa.pk}/'})


class MovimientoPuntosForm(forms.ModelForm):
    class Meta:
        model = MovimientoPuntos
        fields = '__all__'
        widgets = {
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'puntos': forms.NumberInput(attrs={'class': 'form-control'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
        }


@login_required
def movimiento_list(request):
    movimientos = MovimientoPuntos.objects.select_related('propietario').order_by('-id')
    paginator = Paginator(movimientos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'fidelizacion/movimientos.html', {'page_obj': page_obj, 'movimientos': movimientos})


@login_required
def movimiento_create(request):
    if request.method == 'POST':
        form = MovimientoPuntosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento de puntos creado')
            return redirect('movimiento_list')
    else:
        form = MovimientoPuntosForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nuevo Movimiento de Puntos', 'cancel_url': '/fidelizacion/movimiento/'})


@login_required
def movimiento_detail(request, pk):
    movimiento = get_object_or_404(MovimientoPuntos, pk=pk)
    fields = [
        {'label': 'Propietario', 'value': movimiento.propietario.nombre},
        {'label': 'Tipo', 'value': movimiento.get_tipo_display()},
        {'label': 'Puntos', 'value': movimiento.puntos},
        {'label': 'Concepto', 'value': movimiento.concepto},
        {'label': 'Fecha', 'value': movimiento.fecha},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Movimiento Puntos - {movimiento.concepto}",
        'fields': fields,
        'edit_url': f'/fidelizacion/movimiento/{movimiento.pk}/editar/',
        'delete_url': f'/fidelizacion/movimiento/{movimiento.pk}/eliminar/',
        'list_url': '/fidelizacion/movimiento/',
    })


@login_required
def movimiento_update(request, pk):
    movimiento = get_object_or_404(MovimientoPuntos, pk=pk)
    if request.method == 'POST':
        form = MovimientoPuntosForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento de puntos actualizado')
            return redirect('movimiento_detail', pk=movimiento.pk)
    else:
        form = MovimientoPuntosForm(instance=movimiento)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Movimiento de Puntos', 'cancel_url': f'/fidelizacion/movimiento/{movimiento.pk}/'})


@login_required
def movimiento_delete(request, pk):
    movimiento = get_object_or_404(MovimientoPuntos, pk=pk)
    if request.method == 'POST':
        movimiento.delete()
        messages.success(request, 'Movimiento de puntos eliminado')
        return redirect('movimiento_list')
    return render(request, 'generic/delete.html', {'object': movimiento, 'cancel_url': f'/fidelizacion/movimiento/{movimiento.pk}/'})
