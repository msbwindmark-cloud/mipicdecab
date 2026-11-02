from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Transporte
from caballos.models import Caballo
from propietarios.models import Propietario


@login_required
def transporte_list(request):
    query = request.GET.get('q', '')
    transportes = Transporte.objects.select_related('caballo', 'propietario').order_by('-id')
    if query:
        transportes = transportes.filter(
            Q(caballo__nombre__icontains=query) |
            Q(origen__icontains=query) |
            Q(destino__icontains=query) |
            Q(transportista__icontains=query)
        )
    paginator = Paginator(transportes, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'transporte/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'transporte/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def transporte_programar(request):
    if request.method == 'POST':
        Transporte.objects.create(
            caballo_id=request.POST.get('caballo'),
            propietario_id=request.POST.get('propietario') or None,
            tipo=request.POST.get('tipo'),
            fecha_salida=request.POST.get('fecha_salida'),
            origen=request.POST.get('origen'),
            destino=request.POST.get('destino'),
            transportista=request.POST.get('transportista', ''),
            vehiculo=request.POST.get('vehiculo', ''),
            coste=request.POST.get('coste', 0),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Transporte programado')
        return redirect('transporte_list')
    caballos = Caballo.objects.all()
    propietarios = Propietario.objects.filter(activo=True)
    return render(request, 'transporte/programar.html', {'caballos': caballos, 'propietarios': propietarios})


class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_salida': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_llegada': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'transportista': forms.TextInput(attrs={'class': 'form-control'}),
            'vehiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'coste': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def transporte_create(request):
    if request.method == 'POST':
        form = TransporteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transporte programado')
            return redirect('transporte_list')
    else:
        form = TransporteForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nuevo Transporte', 'cancel_url': '/transporte/'})


@login_required
def transporte_detail(request, pk):
    transporte = get_object_or_404(Transporte, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': transporte.caballo.nombre},
        {'label': 'Propietario', 'value': str(transporte.propietario) if transporte.propietario else '-'},
        {'label': 'Tipo', 'value': transporte.get_tipo_display()},
        {'label': 'Fecha Salida', 'value': transporte.fecha_salida},
        {'label': 'Fecha Llegada', 'value': transporte.fecha_llegada or '-'},
        {'label': 'Origen', 'value': transporte.origen},
        {'label': 'Destino', 'value': transporte.destino},
        {'label': 'Transportista', 'value': transporte.transportista or '-'},
        {'label': 'Vehiculo', 'value': transporte.vehiculo or '-'},
        {'label': 'Coste', 'value': transporte.coste},
        {'label': 'Estado', 'value': transporte.get_estado_display()},
        {'label': 'Notas', 'value': transporte.notas or '-'},
        {'label': 'Duracion', 'value': str(transporte.duracion) if transporte.duracion else '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Transporte - {transporte.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/transporte/{transporte.pk}/editar/',
        'delete_url': f'/transporte/{transporte.pk}/eliminar/',
        'list_url': '/transporte/',
    })


@login_required
def transporte_update(request, pk):
    transporte = get_object_or_404(Transporte, pk=pk)
    if request.method == 'POST':
        form = TransporteForm(request.POST, instance=transporte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transporte actualizado')
            return redirect('transporte_detail', pk=transporte.pk)
    else:
        form = TransporteForm(instance=transporte)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Transporte', 'cancel_url': f'/transporte/{transporte.pk}/'})


@login_required
def transporte_delete(request, pk):
    transporte = get_object_or_404(Transporte, pk=pk)
    if request.method == 'POST':
        transporte.delete()
        messages.success(request, 'Transporte eliminado')
        return redirect('transporte_list')
    return render(request, 'generic/delete.html', {'object': transporte, 'cancel_url': f'/transporte/{transporte.pk}/'})
