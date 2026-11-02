from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Encuesta


@login_required
def encuesta_list(request):
    query = request.GET.get('q', '')
    encuestas = Encuesta.objects.order_by('-id')
    if query:
        encuestas = encuestas.filter(
            Q(titulo__icontains=query) |
            Q(tipo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    paginator = Paginator(encuestas, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    if request.htmx:
        return render(request, 'encuestas/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'encuestas/list.html', {'page_obj': page_obj, 'query': query})


class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def encuesta_create(request):
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encuesta creada')
            return redirect('encuesta_list')
    else:
        form = EncuestaForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nueva Encuesta', 'cancel_url': '/encuestas/'})


@login_required
def encuesta_detail(request, pk):
    encuesta = get_object_or_404(Encuesta, pk=pk)
    fields = [
        {'label': 'Titulo', 'value': encuesta.titulo},
        {'label': 'Tipo', 'value': encuesta.get_tipo_display()},
        {'label': 'Fecha Inicio', 'value': encuesta.fecha_inicio},
        {'label': 'Fecha Fin', 'value': encuesta.fecha_fin or '-'},
        {'label': 'Activa', 'value': 'Si' if encuesta.activa else 'No'},
        {'label': 'Total Respuestas', 'value': encuesta.total_respuestas},
        {'label': 'Descripcion', 'value': encuesta.descripcion or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Encuesta - {encuesta.titulo}",
        'fields': fields,
        'edit_url': f'/encuestas/{encuesta.pk}/editar/',
        'delete_url': f'/encuestas/{encuesta.pk}/eliminar/',
        'list_url': '/encuestas/',
    })


@login_required
def encuesta_update(request, pk):
    encuesta = get_object_or_404(Encuesta, pk=pk)
    if request.method == 'POST':
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encuesta actualizada')
            return redirect('encuesta_detail', pk=encuesta.pk)
    else:
        form = EncuestaForm(instance=encuesta)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Encuesta', 'cancel_url': f'/encuestas/{encuesta.pk}/'})


@login_required
def encuesta_delete(request, pk):
    encuesta = get_object_or_404(Encuesta, pk=pk)
    if request.method == 'POST':
        encuesta.delete()
        messages.success(request, 'Encuesta eliminada')
        return redirect('encuesta_list')
    return render(request, 'generic/delete.html', {'object': encuesta, 'cancel_url': f'/encuestas/{encuesta.pk}/'})
