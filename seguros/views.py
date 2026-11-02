from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Seguro
from caballos.models import Caballo


@login_required
def seguro_list(request):
    query = request.GET.get('q', '')
    seguros = Seguro.objects.select_related('caballo').order_by('-id')
    if query:
        seguros = seguros.filter(
            Q(caballo__nombre__icontains=query) |
            Q(compania__icontains=query) |
            Q(numero_poliza__icontains=query) |
            Q(tipo__icontains=query)
        )
    paginator = Paginator(seguros, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'seguros/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'seguros/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def seguro_create(request):
    if request.method == 'POST':
        Seguro.objects.create(
            caballo_id=request.POST.get('caballo'),
            tipo=request.POST.get('tipo'),
            compania=request.POST.get('compania'),
            numero_poliza=request.POST.get('numero_poliza'),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_vencimiento=request.POST.get('fecha_vencimiento'),
            importe=request.POST.get('importe'),
            cobertura=request.POST.get('cobertura'),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Seguro creado')
        return redirect('seguro_list')
    caballos = Caballo.objects.all()
    return render(request, 'seguros/create.html', {'caballos': caballos})


class SeguroForm(forms.ModelForm):
    class Meta:
        model = Seguro
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'compania': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_poliza': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'importe': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'cobertura': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def seguro_detail(request, pk):
    seguro = get_object_or_404(Seguro, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': seguro.caballo.nombre},
        {'label': 'Tipo', 'value': seguro.get_tipo_display()},
        {'label': 'Compania', 'value': seguro.compania},
        {'label': 'Numero Poliza', 'value': seguro.numero_poliza},
        {'label': 'Fecha Inicio', 'value': seguro.fecha_inicio},
        {'label': 'Fecha Vencimiento', 'value': seguro.fecha_vencimiento},
        {'label': 'Importe', 'value': seguro.importe},
        {'label': 'Cobertura', 'value': seguro.cobertura},
        {'label': 'Notas', 'value': seguro.notas or '-'},
        {'label': 'Vencido', 'value': 'Si' if seguro.vencido else 'No'},
        {'label': 'Dias Para Vencimiento', 'value': seguro.dias_para_vencimiento},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Seguro - {seguro.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/seguros/{seguro.pk}/editar/',
        'delete_url': f'/seguros/{seguro.pk}/eliminar/',
        'list_url': '/seguros/',
    })


@login_required
def seguro_update(request, pk):
    seguro = get_object_or_404(Seguro, pk=pk)
    if request.method == 'POST':
        form = SeguroForm(request.POST, instance=seguro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seguro actualizado')
            return redirect('seguro_detail', pk=seguro.pk)
    else:
        form = SeguroForm(instance=seguro)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Seguro', 'cancel_url': f'/seguros/{seguro.pk}/'})


@login_required
def seguro_delete(request, pk):
    seguro = get_object_or_404(Seguro, pk=pk)
    if request.method == 'POST':
        seguro.delete()
        messages.success(request, 'Seguro eliminado')
        return redirect('seguro_list')
    return render(request, 'generic/delete.html', {'object': seguro, 'cancel_url': f'/seguros/{seguro.pk}/'})
