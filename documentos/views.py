from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Documento
from caballos.models import Caballo
from propietarios.models import Propietario


@login_required
def documento_list(request):
    query = request.GET.get('q', '')
    documentos = Documento.objects.select_related('caballo', 'propietario').order_by('-id')
    if query:
        documentos = documentos.filter(
            Q(titulo__icontains=query) |
            Q(tipo__icontains=query) |
            Q(caballo__nombre__icontains=query) |
            Q(propietario__nombre__icontains=query)
        )
    paginator = Paginator(documentos, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'documentos/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'documentos/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def documento_subir(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        Documento.objects.create(
            titulo=request.POST.get('titulo'),
            tipo=request.POST.get('tipo'),
            archivo=request.FILES['archivo'],
            caballo_id=request.POST.get('caballo') or None,
            propietario_id=request.POST.get('propietario') or None,
            fecha_documento=request.POST.get('fecha_documento') or None,
            notas=request.POST.get('notas', ''),
            subido_por=request.user.username,
        )
        messages.success(request, 'Documento subido')
        return redirect('documento_list')
    caballos = Caballo.objects.all()
    propietarios = Propietario.objects.all()
    return render(request, 'documentos/subir.html', {'caballos': caballos, 'propietarios': propietarios})


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'fecha_documento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'subido_por': forms.TextInput(attrs={'class': 'form-control'}),
        }


@login_required
def documento_create(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento subido')
            return redirect('documento_list')
    else:
        form = DocumentoForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Subir Documento', 'cancel_url': '/documentos/'})


@login_required
def documento_detail(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    fields = [
        {'label': 'Titulo', 'value': documento.titulo},
        {'label': 'Tipo', 'value': documento.get_tipo_display()},
        {'label': 'Archivo', 'value': documento.archivo.name if documento.archivo else '-'},
        {'label': 'Caballo', 'value': documento.caballo.nombre if documento.caballo else '-'},
        {'label': 'Propietario', 'value': documento.propietario.nombre if documento.propietario else '-'},
        {'label': 'Fecha Subida', 'value': documento.fecha_subida},
        {'label': 'Fecha Documento', 'value': documento.fecha_documento or '-'},
        {'label': 'Notas', 'value': documento.notas or '-'},
        {'label': 'Subido Por', 'value': documento.subido_por or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Documento - {documento.titulo}",
        'fields': fields,
        'edit_url': f'/documentos/{documento.pk}/editar/',
        'delete_url': f'/documentos/{documento.pk}/eliminar/',
        'list_url': '/documentos/',
    })


@login_required
def documento_update(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento actualizado')
            return redirect('documento_detail', pk=documento.pk)
    else:
        form = DocumentoForm(instance=documento)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Documento', 'cancel_url': f'/documentos/{documento.pk}/'})


@login_required
def documento_delete(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        documento.archivo.delete(save=False)
        documento.delete()
        messages.success(request, 'Documento eliminado')
        return redirect('documento_list')
    return render(request, 'generic/delete.html', {'object': documento, 'cancel_url': f'/documentos/{documento.pk}/'})
