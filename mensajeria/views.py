from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.utils import timezone
from .models import Conversacion, Mensaje
from django.contrib.auth.models import User


@login_required
def mensajeria_list(request):
    query = request.GET.get('q', '')
    conversaciones = Conversacion.objects.filter(participantes=request.user).order_by('-id')
    if query:
        conversaciones = conversaciones.filter(
            Q(mensajes__contenido__icontains=query)
        ).distinct()
    paginator = Paginator(conversaciones, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'mensajeria/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'mensajeria/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        destinatario_id = request.POST.get('destinatario')
        contenido = request.POST.get('contenido')
        destinatario = User.objects.get(pk=destinatario_id)
        
        conversacion = None
        for conv in Conversacion.objects.filter(participantes=request.user):
            if destinatario in conv.participantes.all():
                conversacion = conv
                break
        
        if not conversacion:
            conversacion = Conversacion.objects.create()
            conversacion.participantes.add(request.user, destinatario)
        
        Mensaje.objects.create(conversacion=conversacion, autor=request.user, contenido=contenido)
        conversacion.ultimo_mensaje = timezone.now()
        conversacion.save()
        messages.success(request, 'Mensaje enviado')
        return redirect('mensajeria_list')
    
    usuarios = User.objects.exclude(id=request.user.id).filter(is_active=True)
    return render(request, 'mensajeria/enviar.html', {'usuarios': usuarios})


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = '__all__'
        widgets = {
            'conversacion': forms.Select(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'leido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def mensaje_list(request):
    query = request.GET.get('q', '')
    mensajes = Mensaje.objects.filter(conversacion__participantes=request.user).select_related('conversacion', 'autor').order_by('-fecha')
    if query:
        mensajes = mensajes.filter(Q(contenido__icontains=query))
    paginator = Paginator(mensajes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mensajeria/mensajes.html', {'page_obj': page_obj, 'query': query, 'mensajes': mensajes})


@login_required
def mensaje_create(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje creado')
            return redirect('mensaje_list')
    else:
        form = MensajeForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Nuevo Mensaje', 'cancel_url': '/mensajeria/'})


@login_required
def mensaje_detail(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk)
    fields = [
        {'label': 'Conversacion', 'value': mensaje.conversacion_id},
        {'label': 'Autor', 'value': mensaje.autor.username},
        {'label': 'Contenido', 'value': mensaje.contenido},
        {'label': 'Fecha', 'value': mensaje.fecha},
        {'label': 'Leido', 'value': 'Si' if mensaje.leido else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Mensaje - {mensaje.autor.username}",
        'fields': fields,
        'edit_url': f'/mensajeria/mensaje/{mensaje.pk}/editar/',
        'delete_url': f'/mensajeria/mensaje/{mensaje.pk}/eliminar/',
        'list_url': '/mensajeria/',
    })


@login_required
def mensaje_update(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk)
    if request.method == 'POST':
        form = MensajeForm(request.POST, instance=mensaje)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje actualizado')
            return redirect('mensaje_detail', pk=mensaje.pk)
    else:
        form = MensajeForm(instance=mensaje)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Mensaje', 'cancel_url': f'/mensajeria/mensaje/{mensaje.pk}/'})


@login_required
def mensaje_delete(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk)
    if request.method == 'POST':
        mensaje.delete()
        messages.success(request, 'Mensaje eliminado')
        return redirect('mensaje_list')
    return render(request, 'generic/delete.html', {'object': mensaje, 'cancel_url': f'/mensajeria/mensaje/{mensaje.pk}/'})
