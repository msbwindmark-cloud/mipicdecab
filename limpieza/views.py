from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import LimpiezaBox, ProgramaLimpieza
from instalaciones.models import Box


@login_required
def limpieza_list(request):
    query = request.GET.get('q', '')
    limpiezas = LimpiezaBox.objects.select_related('box').order_by('-id')
    if query:
        limpiezas = limpiezas.filter(
            Q(box__numero__icontains=query) |
            Q(tipo__icontains=query) |
            Q(realizada_por__icontains=query)
        )
    paginator = Paginator(limpiezas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    programa = ProgramaLimpieza.objects.select_related('box').filter(activo=True)
    
    if request.htmx:
        return render(request, 'limpieza/_lista.html', {'page_obj': page_obj, 'query': query, 'programa': programa})
    return render(request, 'limpieza/list.html', {'page_obj': page_obj, 'query': query, 'programa': programa})


@login_required
def registrar_limpieza(request):
    if request.method == 'POST':
        box = Box.objects.get(pk=request.POST.get('box'))
        LimpiezaBox.objects.create(
            box=box,
            tipo=request.POST.get('tipo'),
            realizada_por=request.POST.get('realizada_por', ''),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Limpieza registrada')
        return redirect('limpieza_list')
    boxes = Box.objects.all()
    return render(request, 'limpieza/registrar.html', {'boxes': boxes})


class LimpiezaBoxForm(forms.ModelForm):
    class Meta:
        model = LimpiezaBox
        fields = '__all__'
        widgets = {
            'box': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'realizada_por': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def limpieza_create(request):
    if request.method == 'POST':
        form = LimpiezaBoxForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Limpieza registrada')
            return redirect('limpieza_list')
    else:
        form = LimpiezaBoxForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Registrar Limpieza', 'cancel_url': '/limpieza/'})


@login_required
def limpieza_detail(request, pk):
    limpieza = get_object_or_404(LimpiezaBox, pk=pk)
    fields = [
        {'label': 'Box', 'value': f"Box {limpieza.box.numero}"},
        {'label': 'Tipo', 'value': limpieza.get_tipo_display()},
        {'label': 'Fecha', 'value': limpieza.fecha},
        {'label': 'Realizada Por', 'value': limpieza.realizada_por or '-'},
        {'label': 'Notas', 'value': limpieza.notas or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Limpieza - Box {limpieza.box.numero}",
        'fields': fields,
        'edit_url': f'/limpieza/{limpieza.pk}/editar/',
        'delete_url': f'/limpieza/{limpieza.pk}/eliminar/',
        'list_url': '/limpieza/',
    })


@login_required
def limpieza_update(request, pk):
    limpieza = get_object_or_404(LimpiezaBox, pk=pk)
    if request.method == 'POST':
        form = LimpiezaBoxForm(request.POST, instance=limpieza)
        if form.is_valid():
            form.save()
            messages.success(request, 'Limpieza actualizada')
            return redirect('limpieza_detail', pk=limpieza.pk)
    else:
        form = LimpiezaBoxForm(instance=limpieza)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Limpieza', 'cancel_url': f'/limpieza/{limpieza.pk}/'})


@login_required
def limpieza_delete(request, pk):
    limpieza = get_object_or_404(LimpiezaBox, pk=pk)
    if request.method == 'POST':
        limpieza.delete()
        messages.success(request, 'Limpieza eliminada')
        return redirect('limpieza_list')
    return render(request, 'generic/delete.html', {'object': limpieza, 'cancel_url': f'/limpieza/{limpieza.pk}/'})


class ProgramaLimpiezaForm(forms.ModelForm):
    class Meta:
        model = ProgramaLimpieza
        fields = '__all__'
        widgets = {
            'box': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'frecuencia': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def programa_create(request):
    if request.method == 'POST':
        form = ProgramaLimpiezaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programa de limpieza creado')
            return redirect('limpieza_list')
    else:
        form = ProgramaLimpiezaForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nuevo Programa de Limpieza', 'cancel_url': '/limpieza/'})


@login_required
def programa_detail(request, pk):
    programa = get_object_or_404(ProgramaLimpieza, pk=pk)
    fields = [
        {'label': 'Box', 'value': f"Box {programa.box.numero}"},
        {'label': 'Tipo', 'value': programa.get_tipo_display()},
        {'label': 'Frecuencia', 'value': programa.get_frecuencia_display()},
        {'label': 'Ultima Limpieza', 'value': programa.ultima_limpieza or '-'},
        {'label': 'Proxima Limpieza', 'value': programa.proxima_limpieza or '-'},
        {'label': 'Activo', 'value': 'Si' if programa.activo else 'No'},
        {'label': 'Vencida', 'value': 'Si' if programa.vencida else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Programa Limpieza - Box {programa.box.numero}",
        'fields': fields,
        'edit_url': f'/limpieza/programa/{programa.pk}/editar/',
        'delete_url': f'/limpieza/programa/{programa.pk}/eliminar/',
        'list_url': '/limpieza/',
    })


@login_required
def programa_update(request, pk):
    programa = get_object_or_404(ProgramaLimpieza, pk=pk)
    if request.method == 'POST':
        form = ProgramaLimpiezaForm(request.POST, instance=programa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programa de limpieza actualizado')
            return redirect('programa_detail', pk=programa.pk)
    else:
        form = ProgramaLimpiezaForm(instance=programa)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Programa de Limpieza', 'cancel_url': f'/limpieza/programa/{programa.pk}/'})


@login_required
def programa_delete(request, pk):
    programa = get_object_or_404(ProgramaLimpieza, pk=pk)
    if request.method == 'POST':
        programa.delete()
        messages.success(request, 'Programa de limpieza eliminado')
        return redirect('limpieza_list')
    return render(request, 'generic/delete.html', {'object': programa, 'cancel_url': f'/limpieza/programa/{programa.pk}/'})
