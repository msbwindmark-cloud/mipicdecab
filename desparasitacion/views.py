from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import PlanDesparasitacion, RegistroDesparasitacion
from caballos.models import Caballo
import datetime


@login_required
def desparasitacion_list(request):
    query = request.GET.get('q', '')
    planes = PlanDesparasitacion.objects.select_related('caballo').order_by('-id')
    if query:
        planes = planes.filter(
            Q(caballo__nombre__icontains=query) |
            Q(producto__icontains=query) |
            Q(tipo__icontains=query)
        )
    paginator = Paginator(planes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'desparasitacion/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'desparasitacion/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def registrar_desparasitacion(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        plan = PlanDesparasitacion.objects.get(pk=plan_id)
        RegistroDesparasitacion.objects.create(
            plan=plan,
            producto_usado=request.POST.get('producto_usado'),
            dosis=request.POST.get('dosis'),
            coste=request.POST.get('coste', 0),
            realizado_por=request.POST.get('realizado_por', ''),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Desparasitación registrada')
        return redirect('desparasitacion_list')
    planes = PlanDesparasitacion.objects.select_related('caballo').all()
    return render(request, 'desparasitacion/registrar.html', {'planes': planes})


class PlanDesparasitacionForm(forms.ModelForm):
    class Meta:
        model = PlanDesparasitacion
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.Select(attrs={'class': 'form-control'}),
            'ultima_desparasitacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'proxima_desparasitacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def plan_create(request):
    if request.method == 'POST':
        form = PlanDesparasitacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan de desparasitación creado')
            return redirect('desparasitacion_list')
    else:
        form = PlanDesparasitacionForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nuevo Plan de Desparasitación', 'cancel_url': '/desparasitacion/'})


@login_required
def plan_detail(request, pk):
    plan = get_object_or_404(PlanDesparasitacion, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': plan.caballo.nombre},
        {'label': 'Tipo', 'value': plan.get_tipo_display()},
        {'label': 'Producto', 'value': plan.producto},
        {'label': 'Frecuencia', 'value': plan.get_frecuencia_display()},
        {'label': 'Ultima Desparasitacion', 'value': plan.ultima_desparasitacion or '-'},
        {'label': 'Proxima Desparasitacion', 'value': plan.proxima_desparasitacion or '-'},
        {'label': 'Activo', 'value': 'Si' if plan.activo else 'No'},
        {'label': 'Notas', 'value': plan.notas or '-'},
        {'label': 'Vencida', 'value': 'Si' if plan.vencida else 'No'},
        {'label': 'Dias Para', 'value': plan.dias_para},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Plan Desparasitación - {plan.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/desparasitacion/plan/{plan.pk}/editar/',
        'delete_url': f'/desparasitacion/plan/{plan.pk}/eliminar/',
        'list_url': '/desparasitacion/',
    })


@login_required
def plan_update(request, pk):
    plan = get_object_or_404(PlanDesparasitacion, pk=pk)
    if request.method == 'POST':
        form = PlanDesparasitacionForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan de desparasitación actualizado')
            return redirect('plan_detail', pk=plan.pk)
    else:
        form = PlanDesparasitacionForm(instance=plan)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Plan de Desparasitación', 'cancel_url': f'/desparasitacion/plan/{plan.pk}/'})


@login_required
def plan_delete(request, pk):
    plan = get_object_or_404(PlanDesparasitacion, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plan de desparasitación eliminado')
        return redirect('desparasitacion_list')
    return render(request, 'generic/delete.html', {'object': plan, 'cancel_url': f'/desparasitacion/plan/{plan.pk}/'})


class RegistroDesparasitacionForm(forms.ModelForm):
    class Meta:
        model = RegistroDesparasitacion
        fields = '__all__'
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'producto_usado': forms.TextInput(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'realizado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def registro_detail(request, pk):
    registro = get_object_or_404(RegistroDesparasitacion, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': registro.plan.caballo.nombre},
        {'label': 'Fecha', 'value': registro.fecha},
        {'label': 'Producto Usado', 'value': registro.producto_usado},
        {'label': 'Dosis', 'value': registro.dosis},
        {'label': 'Coste', 'value': registro.coste},
        {'label': 'Realizado Por', 'value': registro.realizado_por or '-'},
        {'label': 'Notas', 'value': registro.notas or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Desparasitación - {registro.plan.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/desparasitacion/registro/{registro.pk}/editar/',
        'delete_url': f'/desparasitacion/registro/{registro.pk}/eliminar/',
        'list_url': '/desparasitacion/',
    })


@login_required
def registro_update(request, pk):
    registro = get_object_or_404(RegistroDesparasitacion, pk=pk)
    if request.method == 'POST':
        form = RegistroDesparasitacionForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Desparasitación registrada')
            return redirect('registro_detail', pk=registro.pk)
    else:
        form = RegistroDesparasitacionForm(instance=registro)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Registro de Desparasitación', 'cancel_url': f'/desparasitacion/registro/{registro.pk}/'})


@login_required
def registro_delete(request, pk):
    registro = get_object_or_404(RegistroDesparasitacion, pk=pk)
    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Registro de desparasitación eliminado')
        return redirect('desparasitacion_list')
    return render(request, 'generic/delete.html', {'object': registro, 'cancel_url': f'/desparasitacion/registro/{registro.pk}/'})
