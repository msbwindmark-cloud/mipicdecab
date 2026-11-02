from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Evento


@login_required
def evento_list(request):
    query = request.GET.get('q', '')
    eventos = Evento.objects.order_by('-id')
    if query:
        eventos = eventos.filter(
            Q(nombre__icontains=query) |
            Q(tipo__icontains=query) |
            Q(lugar__icontains=query)
        )
    paginator = Paginator(eventos, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'eventos/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'eventos/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def evento_create(request):
    if request.method == 'POST':
        Evento.objects.create(
            nombre=request.POST.get('nombre'),
            tipo=request.POST.get('tipo'),
            fecha=request.POST.get('fecha'),
            lugar=request.POST.get('lugar'),
            descripcion=request.POST.get('descripcion'),
        )
        messages.success(request, 'Evento creado')
        return redirect('evento_list')
    return render(request, 'eventos/create.html', {})


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def evento_detail(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    fields = [
        {'label': 'Nombre', 'value': evento.nombre},
        {'label': 'Tipo', 'value': evento.get_tipo_display()},
        {'label': 'Fecha', 'value': evento.fecha},
        {'label': 'Lugar', 'value': evento.lugar},
        {'label': 'Descripcion', 'value': evento.descripcion or '-'},
        {'label': 'Caballos', 'value': evento.caballos.count()},
        {'label': 'Propietarios', 'value': evento.propietarios.count},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Evento - {evento.nombre}",
        'fields': fields,
        'edit_url': f'/eventos/{evento.pk}/editar/',
        'delete_url': f'/eventos/{evento.pk}/eliminar/',
        'list_url': '/eventos/',
    })


@login_required
def evento_update(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado')
            return redirect('evento_detail', pk=evento.pk)
    else:
        form = EventoForm(instance=evento)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Evento', 'cancel_url': f'/eventos/{evento.pk}/'})


@login_required
def evento_delete(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado')
        return redirect('evento_list')
    return render(request, 'generic/delete.html', {'object': evento, 'cancel_url': f'/eventos/{evento.pk}/'})
