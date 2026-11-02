from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Proveedor, PedidoProveedor


@login_required
def proveedor_list(request):
    query = request.GET.get('q', '')
    proveedores = Proveedor.objects.order_by('-id')
    if query:
        proveedores = proveedores.filter(
            Q(nombre__icontains=query) |
            Q(tipo__icontains=query) |
            Q(contacto__icontains=query) |
            Q(telefono__icontains=query)
        )
    paginator = Paginator(proveedores, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    pedidos = PedidoProveedor.objects.select_related('proveedor').all()
    
    if request.htmx:
        return render(request, 'proveedores/_lista.html', {'page_obj': page_obj, 'query': query, 'pedidos': pedidos})
    return render(request, 'proveedores/list.html', {'page_obj': page_obj, 'query': query, 'pedidos': pedidos})


@login_required
def proveedor_create(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre=request.POST.get('nombre'),
            tipo=request.POST.get('tipo'),
            contacto=request.POST.get('contacto', ''),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email', ''),
            direccion=request.POST.get('direccion', ''),
            cif_nif=request.POST.get('cif_nif', ''),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Proveedor creado')
        return redirect('proveedor_list')
    return render(request, 'proveedores/create.html', {})


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'cif_nif': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def proveedor_detail(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    fields = [
        {'label': 'Nombre', 'value': proveedor.nombre},
        {'label': 'Tipo', 'value': proveedor.get_tipo_display()},
        {'label': 'Contacto', 'value': proveedor.contacto or '-'},
        {'label': 'Telefono', 'value': proveedor.telefono},
        {'label': 'Email', 'value': proveedor.email or '-'},
        {'label': 'Direccion', 'value': proveedor.direccion or '-'},
        {'label': 'CIF/NIF', 'value': proveedor.cif_nif or '-'},
        {'label': 'Notas', 'value': proveedor.notas or '-'},
        {'label': 'Activo', 'value': 'Si' if proveedor.activo else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Proveedor - {proveedor.nombre}",
        'fields': fields,
        'edit_url': f'/proveedores/{proveedor.pk}/editar/',
        'delete_url': f'/proveedores/{proveedor.pk}/eliminar/',
        'list_url': '/proveedores/',
    })


@login_required
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado')
            return redirect('proveedor_detail', pk=proveedor.pk)
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Proveedor', 'cancel_url': f'/proveedores/{proveedor.pk}/'})


@login_required
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado')
        return redirect('proveedor_list')
    return render(request, 'generic/delete.html', {'object': proveedor, 'cancel_url': f'/proveedores/{proveedor.pk}/'})
