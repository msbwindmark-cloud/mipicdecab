from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django import forms
from .models import GastoCaballo
from caballos.models import Caballo


@login_required
def gasto_list(request):
    query = request.GET.get('q', '')
    gastos = GastoCaballo.objects.select_related('caballo').order_by('-id')
    if query:
        gastos = gastos.filter(
            Q(caballo__nombre__icontains=query) |
            Q(concepto__icontains=query) |
            Q(categoria__icontains=query) |
            Q(proveedor__icontains=query)
        )
    total = gastos.aggregate(total=Sum('importe'))['total'] or 0
    paginator = Paginator(gastos, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'gastos_caballo/_lista.html', {'page_obj': page_obj, 'query': query, 'total': total})
    return render(request, 'gastos_caballo/list.html', {'page_obj': page_obj, 'query': query, 'total': total})


@login_required
def gasto_create(request):
    if request.method == 'POST':
        GastoCaballo.objects.create(
            caballo_id=request.POST.get('caballo'),
            categoria=request.POST.get('categoria'),
            concepto=request.POST.get('concepto'),
            importe=request.POST.get('importe'),
            fecha=request.POST.get('fecha'),
            proveedor=request.POST.get('proveedor', ''),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Gasto registrado')
        return redirect('gasto_list')
    caballos = Caballo.objects.all()
    return render(request, 'gastos_caballo/create.html', {'caballos': caballos})


class GastoCaballoForm(forms.ModelForm):
    class Meta:
        model = GastoCaballo
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'importe': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def gasto_detail(request, pk):
    gasto = get_object_or_404(GastoCaballo, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': gasto.caballo.nombre},
        {'label': 'Categoria', 'value': gasto.get_categoria_display()},
        {'label': 'Concepto', 'value': gasto.concepto},
        {'label': 'Importe', 'value': gasto.importe},
        {'label': 'Fecha', 'value': gasto.fecha},
        {'label': 'Proveedor', 'value': gasto.proveedor or '-'},
        {'label': 'Notas', 'value': gasto.notas or '-'},
        {'label': 'Total Gastos Caballo', 'value': gasto.total_gastos_caballo},
    ]
    return render(request, 'generic/detail.html', {
        'title': f" Gasto - {gasto.concepto}",
        'fields': fields,
        'edit_url': f'/gastos/{gasto.pk}/editar/',
        'delete_url': f'/gastos/{gasto.pk}/eliminar/',
        'list_url': '/gastos/',
    })


@login_required
def gasto_update(request, pk):
    gasto = get_object_or_404(GastoCaballo, pk=pk)
    if request.method == 'POST':
        form = GastoCaballoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto actualizado')
            return redirect('gasto_detail', pk=gasto.pk)
    else:
        form = GastoCaballoForm(instance=gasto)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Gasto', 'cancel_url': f'/gastos/{gasto.pk}/'})


@login_required
def gasto_delete(request, pk):
    gasto = get_object_or_404(GastoCaballo, pk=pk)
    if request.method == 'POST':
        gasto.delete()
        messages.success(request, 'Gasto eliminado')
        return redirect('gasto_list')
    return render(request, 'generic/delete.html', {'object': gasto, 'cancel_url': f'/gastos/{gasto.pk}/'})
