from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.utils import timezone
from .models import Empleado, Fichaje, HorarioEmpleado
from django.contrib.auth.models import User


@login_required
def empleado_list(request):
    query = request.GET.get('q', '')
    empleados = Empleado.objects.order_by('-id')
    if query:
        empleados = empleados.filter(
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(puesto__icontains=query) |
            Q(telefono__icontains=query)
        )
    paginator = Paginator(empleados, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'empleados/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'empleados/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado')
            return redirect('empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nuevo Empleado', 'cancel_url': '/empleados/'})


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def empleado_detail(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    fields = [
        {'label': 'Nombre', 'value': empleado.nombre},
        {'label': 'Apellidos', 'value': empleado.apellidos},
        {'label': 'Puesto', 'value': empleado.get_puesto_display()},
        {'label': 'Telefono', 'value': empleado.telefono},
        {'label': 'Email', 'value': empleado.email or '-'},
        {'label': 'Fecha Contratacion', 'value': empleado.fecha_contratacion},
        {'label': 'Salario', 'value': empleado.salario},
        {'label': 'Activo', 'value': 'Si' if empleado.activo else 'No'},
        {'label': 'User', 'value': empleado.user.username if empleado.user else '-'},
        {'label': 'Notas', 'value': empleado.notas or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Empleado - {empleado.nombre} {empleado.apellidos}",
        'fields': fields,
        'edit_url': f'/empleados/{empleado.pk}/editar/',
        'delete_url': f'/empleados/{empleado.pk}/eliminar/',
        'list_url': '/empleados/',
    })


@login_required
def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado')
            return redirect('empleado_detail', pk=empleado.pk)
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Empleado', 'cancel_url': f'/empleados/{empleado.pk}/'})


@login_required
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado')
        return redirect('empleado_list')
    return render(request, 'generic/delete.html', {'object': empleado, 'cancel_url': f'/empleados/{empleado.pk}/'})


@login_required
def fichar(request):
    if request.method == 'POST':
        empleado_id = request.POST.get('empleado')
        tipo = request.POST.get('tipo')
        empleado = Empleado.objects.get(pk=empleado_id)
        Fichaje.objects.create(empleado=empleado, tipo=tipo, notas=request.POST.get('notas', ''))
        messages.success(request, f'Fichaje de {tipo} registrado para {empleado.nombre}')
        return redirect('empleado_list')
    empleados = Empleado.objects.filter(activo=True)
    return render(request, 'empleados/fichar.html', {'empleados': empleados})
