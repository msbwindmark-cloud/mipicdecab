from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.utils import timezone
from .models import Tarea
from django.contrib.auth.models import User


@login_required
def tarea_list(request):
    query = request.GET.get('q', '')
    tareas = Tarea.objects.select_related('caballo', 'asignado_a').order_by('-id')
    if query:
        tareas = tareas.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(prioridad__icontains=query) |
            Q(estado__icontains=query)
        )
    paginator = Paginator(tareas, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'tareas/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'tareas/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def tarea_create(request):
    if request.method == 'POST':
        Tarea.objects.create(
            titulo=request.POST.get('titulo'),
            descripcion=request.POST.get('descripcion'),
            prioridad=request.POST.get('prioridad', 'MEDIA'),
            fecha_limite=request.POST.get('fecha_limite') or None,
            asignado_a_id=request.POST.get('asignado_a') or None,
        )
        messages.success(request, 'Tarea creada')
        return redirect('tarea_list')
    usuarios = User.objects.filter(is_active=True)
    return render(request, 'tareas/create.html', {'usuarios': usuarios})


@login_required
def tarea_completar(request, pk):
    tarea = Tarea.objects.get(pk=pk)
    from django.utils import timezone
    tarea.estado = 'COMPLETADA'
    tarea.fecha_completada = timezone.now()
    tarea.save()
    messages.success(request, 'Tarea completada')
    return redirect('tarea_list')


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'asignado_a': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


@login_required
def tarea_detail(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    fields = [
        {'label': 'Titulo', 'value': tarea.titulo},
        {'label': 'Descripcion', 'value': tarea.descripcion or '-'},
        {'label': 'Caballo', 'value': tarea.caballo.nombre if tarea.caballo else '-'},
        {'label': 'Asignado A', 'value': tarea.asignado_a.username if tarea.asignado_a else '-'},
        {'label': 'Prioridad', 'value': tarea.get_prioridad_display()},
        {'label': 'Estado', 'value': tarea.get_estado_display()},
        {'label': 'Fecha Creacion', 'value': tarea.fecha_creacion},
        {'label': 'Fecha Limite', 'value': tarea.fecha_limite or '-'},
        {'label': 'Fecha Completada', 'value': tarea.fecha_completada or '-'},
        {'label': 'Vencida', 'value': 'Si' if tarea.vencida else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Tarea - {tarea.titulo}",
        'fields': fields,
        'edit_url': f'/tareas/{tarea.pk}/editar/',
        'delete_url': f'/tareas/{tarea.pk}/eliminar/',
        'list_url': '/tareas/',
    })


@login_required
def tarea_update(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada')
            return redirect('tarea_detail', pk=tarea.pk)
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Tarea', 'cancel_url': f'/tareas/{tarea.pk}/'})


@login_required
def tarea_delete(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, 'Tarea eliminada')
        return redirect('tarea_list')
    return render(request, 'generic/delete.html', {'object': tarea, 'cancel_url': f'/tareas/{tarea.pk}/'})
