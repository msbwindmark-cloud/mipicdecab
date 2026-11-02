from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.utils import timezone
from .models import VisitaVeterinaria
from caballos.models import Caballo


@login_required
def visita_list(request):
    query = request.GET.get('q', '')
    visitas = VisitaVeterinaria.objects.select_related('caballo').order_by('-id')
    if query:
        visitas = visitas.filter(
            Q(caballo__nombre__icontains=query) |
            Q(veterinario__icontains=query) |
            Q(motivo__icontains=query) |
            Q(tipo__icontains=query)
        )
    paginator = Paginator(visitas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'visitas_vet/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'visitas_vet/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def visita_programar(request):
    if request.method == 'POST':
        VisitaVeterinaria.objects.create(
            caballo_id=request.POST.get('caballo'),
            veterinario=request.POST.get('veterinario'),
            tipo=request.POST.get('tipo'),
            fecha_programada=request.POST.get('fecha_programada'),
            motivo=request.POST.get('motivo'),
            diagnostico=request.POST.get('diagnostico', ''),
            tratamiento=request.POST.get('tratamiento', ''),
            coste=request.POST.get('coste', 0),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Visita programada')
        return redirect('visita_list')
    caballos = Caballo.objects.all()
    return render(request, 'visitas_vet/programar.html', {'caballos': caballos})


class VisitaVeterinariaForm(forms.ModelForm):
    class Meta:
        model = VisitaVeterinaria
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_programada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_realizada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'tratamiento': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def visita_update(request, pk):
    visita = get_object_or_404(VisitaVeterinaria, pk=pk)
    if request.method == 'POST':
        form = VisitaVeterinariaForm(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visita actualizada')
            return redirect('visita_detail', pk=visita.pk)
    else:
        form = VisitaVeterinariaForm(instance=visita)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Visita Veterinaria', 'cancel_url': f'/visitas-vet/{visita.pk}/'})


@login_required
def visita_detail(request, pk):
    visita = get_object_or_404(VisitaVeterinaria, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': visita.caballo.nombre},
        {'label': 'Veterinario', 'value': visita.veterinario},
        {'label': 'Tipo', 'value': visita.get_tipo_display()},
        {'label': 'Fecha Programada', 'value': visita.fecha_programada},
        {'label': 'Fecha Realizada', 'value': visita.fecha_realizada or '-'},
        {'label': 'Motivo', 'value': visita.motivo},
        {'label': 'Diagnostico', 'value': visita.diagnostico or '-'},
        {'label': 'Tratamiento', 'value': visita.tratamiento or '-'},
        {'label': 'Coste', 'value': visita.coste},
        {'label': 'Estado', 'value': visita.get_estado_display()},
        {'label': 'Notas', 'value': visita.notas or '-'},
        {'label': 'Pendiente', 'value': 'Si' if visita.pendiente else 'No'},
        {'label': 'Vencida', 'value': 'Si' if visita.vencida else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Visita Veterinaria - {visita.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/visitas-vet/{visita.pk}/editar/',
        'delete_url': f'/visitas-vet/{visita.pk}/eliminar/',
        'list_url': '/visitas-vet/',
    })


@login_required
def visita_delete(request, pk):
    visita = get_object_or_404(VisitaVeterinaria, pk=pk)
    if request.method == 'POST':
        visita.delete()
        messages.success(request, 'Visita eliminada')
        return redirect('visita_list')
    return render(request, 'generic/delete.html', {'object': visita, 'cancel_url': f'/visitas-vet/{visita.pk}/'})
