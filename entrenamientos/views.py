from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Entrenamiento


class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'objetivo': forms.TextInput(attrs={'class': 'form-control'}),
            'ejercicios': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'duracion_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'intensidad': forms.Select(attrs={'class': 'form-control'}),
            'completado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def entrenamiento_list(request):
    query = request.GET.get('q', '')
    entrenamientos = Entrenamiento.objects.select_related('caballo').order_by('-fecha')
    if query:
        entrenamientos = entrenamientos.filter(
            Q(caballo__nombre__icontains=query) |
            Q(objetivo__icontains=query) |
            Q(ejercicios__icontains=query)
        )
    paginator = Paginator(entrenamientos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'entrenamientos/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'entrenamientos/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def entrenamiento_create(request):
    if request.method == 'POST':
        form = EntrenamientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrenamiento creado')
            return redirect('entrenamiento_list')
    else:
        form = EntrenamientoForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nuevo Entrenamiento', 'cancel_url': '/entrenamientos/'})


@login_required
def entrenamiento_detail(request, pk):
    entrenamiento = get_object_or_404(Entrenamiento, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': entrenamiento.caballo.nombre},
        {'label': 'Fecha', 'value': entrenamiento.fecha},
        {'label': 'Objetivo', 'value': entrenamiento.objetivo},
        {'label': 'Ejercicios', 'value': entrenamiento.ejercicios or '-'},
        {'label': 'Duracion', 'value': f"{entrenamiento.duracion_min} min"},
        {'label': 'Intensidad', 'value': entrenamiento.get_intensidad_display()},
        {'label': 'Completado', 'value': 'Si' if entrenamiento.completado else 'No'},
        {'label': 'Notas', 'value': entrenamiento.notas or '-'},
        {'label': 'Fecha Creacion', 'value': entrenamiento.fecha_creacion},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Entrenamiento - {entrenamiento.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/entrenamientos/{entrenamiento.pk}/editar/',
        'delete_url': f'/entrenamientos/{entrenamiento.pk}/eliminar/',
        'list_url': '/entrenamientos/',
    })


@login_required
def entrenamiento_update(request, pk):
    entrenamiento = get_object_or_404(Entrenamiento, pk=pk)
    if request.method == 'POST':
        form = EntrenamientoForm(request.POST, instance=entrenamiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrenamiento actualizado')
            return redirect('entrenamiento_detail', pk=entrenamiento.pk)
    else:
        form = EntrenamientoForm(instance=entrenamiento)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Entrenamiento', 'cancel_url': f'/entrenamientos/{entrenamiento.pk}/'})


@login_required
def entrenamiento_delete(request, pk):
    entrenamiento = get_object_or_404(Entrenamiento, pk=pk)
    if request.method == 'POST':
        entrenamiento.delete()
        messages.success(request, 'Entrenamiento eliminado')
        return redirect('entrenamiento_list')
    return render(request, 'generic/delete.html', {'object': entrenamiento, 'cancel_url': f'/entrenamientos/{entrenamiento.pk}/'})
