from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import VentaCaballo
from caballos.models import Caballo
from propietarios.models import Propietario


@login_required
def venta_list(request):
    query = request.GET.get('q', '')
    ventas = VentaCaballo.objects.select_related('caballo', 'comprador').order_by('-id')
    if query:
        ventas = ventas.filter(
            Q(caballo__nombre__icontains=query) |
            Q(estado__icontains=query) |
            Q(descripcion__icontains=query)
        )
    paginator = Paginator(ventas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'ventas/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'ventas/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def venta_publicar(request):
    if request.method == 'POST':
        VentaCaballo.objects.create(
            caballo_id=request.POST.get('caballo'),
            precio_venta=request.POST.get('precio_venta'),
            precio_minimo=request.POST.get('precio_minimo') or None,
            descripcion=request.POST.get('descripcion'),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Caballo publicado en venta')
        return redirect('venta_list')
    caballos = Caballo.objects.all()
    return render(request, 'ventas/publicar.html', {'caballos': caballos})


class VentaCaballoForm(forms.ModelForm):
    class Meta:
        model = VentaCaballo
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'precio_minimo': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'comprador': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


@login_required
def venta_create(request):
    if request.method == 'POST':
        form = VentaCaballoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Caballo publicado en venta')
            return redirect('venta_list')
    else:
        form = VentaCaballoForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Publicar Caballo en Venta', 'cancel_url': '/ventas/'})


@login_required
def venta_detail(request, pk):
    venta = get_object_or_404(VentaCaballo, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': venta.caballo.nombre},
        {'label': 'Precio Venta', 'value': venta.precio_venta},
        {'label': 'Precio Minimo', 'value': venta.precio_minimo or '-'},
        {'label': 'Fecha Publicacion', 'value': venta.fecha_publicacion},
        {'label': 'Fecha Venta', 'value': venta.fecha_venta or '-'},
        {'label': 'Comprador', 'value': str(venta.comprador) if venta.comprador else '-'},
        {'label': 'Estado', 'value': venta.get_estado_display()},
        {'label': 'Descripcion', 'value': venta.descripcion},
        {'label': 'Notas', 'value': venta.notas or '-'},
        {'label': 'Dias En Venta', 'value': venta.dias_en_venta},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Venta - {venta.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/ventas/{venta.pk}/editar/',
        'delete_url': f'/ventas/{venta.pk}/eliminar/',
        'list_url': '/ventas/',
    })


@login_required
def venta_update(request, pk):
    venta = get_object_or_404(VentaCaballo, pk=pk)
    if request.method == 'POST':
        form = VentaCaballoForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venta actualizada')
            return redirect('venta_detail', pk=venta.pk)
    else:
        form = VentaCaballoForm(instance=venta)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Venta', 'cancel_url': f'/ventas/{venta.pk}/'})


@login_required
def venta_delete(request, pk):
    venta = get_object_or_404(VentaCaballo, pk=pk)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada')
        return redirect('venta_list')
    return render(request, 'generic/delete.html', {'object': venta, 'cancel_url': f'/ventas/{venta.pk}/'})
