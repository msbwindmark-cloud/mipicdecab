from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import NotaBitacora
from caballos.models import Caballo


@login_required
def bitacora_list(request):
    query = request.GET.get('q', '')
    notas = NotaBitacora.objects.select_related('caballo', 'autor').order_by('-id')
    if query:
        notas = notas.filter(
            Q(titulo__icontains=query) |
            Q(contenido__icontains=query) |
            Q(tipo__icontains=query) |
            Q(caballo__nombre__icontains=query)
        )
    paginator = Paginator(notas, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'bitacora/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'bitacora/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def bitacora_create(request):
    if request.method == 'POST':
        NotaBitacora.objects.create(
            tipo=request.POST.get('tipo', 'GENERAL'),
            titulo=request.POST.get('titulo'),
            contenido=request.POST.get('contenido'),
            caballo_id=request.POST.get('caballo') or None,
            autor=request.user,
            importante=request.POST.get('importante') == 'on',
        )
        messages.success(request, 'Nota creada')
        return redirect('bitacora_list')
    caballos = Caballo.objects.all()
    return render(request, 'bitacora/create.html', {'caballos': caballos})


class NotaBitacoraForm(forms.ModelForm):
    class Meta:
        model = NotaBitacora
        fields = '__all__'
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def bitacora_update(request, pk):
    nota = get_object_or_404(NotaBitacora, pk=pk)
    if request.method == 'POST':
        form = NotaBitacoraForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nota actualizada')
            return redirect('bitacora_detail', pk=nota.pk)
    else:
        form = NotaBitacoraForm(instance=nota)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Nota', 'cancel_url': f'/bitacora/{nota.pk}/'})


@login_required
def bitacora_detail(request, pk):
    nota = get_object_or_404(NotaBitacora, pk=pk)
    fields = [
        {'label': 'Fecha', 'value': nota.fecha},
        {'label': 'Hora', 'value': nota.hora},
        {'label': 'Tipo', 'value': nota.get_tipo_display()},
        {'label': 'Titulo', 'value': nota.titulo},
        {'label': 'Contenido', 'value': nota.contenido},
        {'label': 'Caballo', 'value': nota.caballo.nombre if nota.caballo else '-'},
        {'label': 'Autor', 'value': nota.autor.username if nota.autor else '-'},
        {'label': 'Importante', 'value': 'Si' if nota.importante else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Bitacora - {nota.titulo}",
        'fields': fields,
        'edit_url': f'/bitacora/{nota.pk}/editar/',
        'delete_url': f'/bitacora/{nota.pk}/eliminar/',
        'list_url': '/bitacora/',
    })


@login_required
def bitacora_delete(request, pk):
    nota = get_object_or_404(NotaBitacora, pk=pk)
    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota eliminada')
        return redirect('bitacora_list')
    return render(request, 'generic/delete.html', {'object': nota, 'cancel_url': f'/bitacora/{nota.pk}/'})
