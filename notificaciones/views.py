from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.utils import timezone
from .models import Notificacion
from django.contrib.auth.models import User


@login_required
def notificacion_list(request):
    query = request.GET.get('q', '')
    notificaciones = Notificacion.objects.filter(destinatario=request.user).order_by('-id')
    if query:
        notificaciones = notificaciones.filter(
            Q(titulo__icontains=query) |
            Q(mensaje__icontains=query) |
            Q(tipo__icontains=query)
        )
    paginator = Paginator(notificaciones, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'notificaciones/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'notificaciones/list.html', {'page_obj': page_obj, 'query': query})


class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = '__all__'
        widgets = {
            'destinatario': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'leida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }


@login_required
def notificacion_create(request):
    if request.method == 'POST':
        form = NotificacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notificación creada')
            return redirect('notificacion_list')
    else:
        form = NotificacionForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nueva Notificación', 'cancel_url': '/notificaciones/'})


@login_required
def notificacion_detail(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk)
    fields = [
        {'label': 'Destinatario', 'value': notificacion.destinatario.username},
        {'label': 'Tipo', 'value': notificacion.get_tipo_display()},
        {'label': 'Titulo', 'value': notificacion.titulo},
        {'label': 'Mensaje', 'value': notificacion.mensaje},
        {'label': 'Leida', 'value': 'Si' if notificacion.leida else 'No'},
        {'label': 'Fecha', 'value': notificacion.fecha},
        {'label': 'Url', 'value': notificacion.url or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Notificación - {notificacion.titulo}",
        'fields': fields,
        'edit_url': f'/notificaciones/{notificacion.pk}/editar/',
        'delete_url': f'/notificaciones/{notificacion.pk}/eliminar/',
        'list_url': '/notificaciones/',
    })


@login_required
def notificacion_update(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk)
    if request.method == 'POST':
        form = NotificacionForm(request.POST, instance=notificacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notificación actualizada')
            return redirect('notificacion_detail', pk=notificacion.pk)
    else:
        form = NotificacionForm(instance=notificacion)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Notificación', 'cancel_url': f'/notificaciones/{notificacion.pk}/'})


@login_required
def notificacion_delete(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk)
    if request.method == 'POST':
        notificacion.delete()
        messages.success(request, 'Notificación eliminada')
        return redirect('notificacion_list')
    return render(request, 'generic/delete.html', {'object': notificacion, 'cancel_url': f'/notificaciones/{notificacion.pk}/'})
