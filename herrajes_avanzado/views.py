from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import VisitaHerrador
from caballos.models import Caballo


@login_required
def herraje_list(request):
    query = request.GET.get('q', '')
    visitas = VisitaHerrador.objects.select_related('caballo').order_by('-id')
    if query:
        visitas = visitas.filter(
            Q(caballo__nombre__icontains=query) |
            Q(herrador__icontains=query) |
            Q(tipo__icontains=query) |
            Q(estado__icontains=query)
        )
    paginator = Paginator(visitas, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    if request.htmx:
        return render(request, 'herrajes_avanzado/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'herrajes_avanzado/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def herraje_programar(request):
    if request.method == 'POST':
        VisitaHerrador.objects.create(
            caballo_id=request.POST.get('caballo'),
            herrador=request.POST.get('herrador'),
            tipo=request.POST.get('tipo'),
            fecha_programada=request.POST.get('fecha_programada'),
            tipo_herradura=request.POST.get('tipo_herradura', ''),
            coste=request.POST.get('coste', 0),
            proximo_herraje=request.POST.get('proximo_herraje') or None,
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Visita de herrador programada')
        return redirect('herraje_list')
    caballos = Caballo.objects.all()
    return render(request, 'herrajes_avanzado/programar.html', {'caballos': caballos})


class VisitaHerradorForm(forms.ModelForm):
    class Meta:
        model = VisitaHerrador
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'herrador': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_programada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_realizada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_herradura': forms.TextInput(attrs={'class': 'form-control'}),
            'coste': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'proximo_herraje': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'caballo': 'Caballo',
            'herrador': 'Herrador',
            'tipo': 'Tipo de Visita',
            'fecha_programada': 'Fecha Programada',
            'fecha_realizada': 'Fecha Realizada',
            'tipo_herradura': 'Tipo de Herradura',
            'coste': 'Coste (€)',
            'proximo_herraje': 'Proximo Herraje',
            'notas': 'Notas',
            'estado': 'Estado',
        }


@login_required
def herraje_create(request):
    if request.method == 'POST':
        form = VisitaHerradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visita de herrador programada')
            return redirect('herraje_list')
    else:
        form = VisitaHerradorForm()
    return render(request, 'generic/form.html', {'form': form, 'title': 'Programar Visita de Herrador', 'cancel_url': '/herrajes-avanzado/'})


@login_required
def herraje_detail(request, pk):
    visita = get_object_or_404(VisitaHerrador, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': visita.caballo.nombre},
        {'label': 'Herrador', 'value': visita.herrador},
        {'label': 'Tipo', 'value': visita.get_tipo_display()},
        {'label': 'Fecha Programada', 'value': visita.fecha_programada},
        {'label': 'Fecha Realizada', 'value': visita.fecha_realizada or '-'},
        {'label': 'Tipo Herradura', 'value': visita.tipo_herradura or '-'},
        {'label': 'Coste', 'value': str(visita.coste)},
        {'label': 'Proximo Herraje', 'value': visita.proximo_herraje or '-'},
        {'label': 'Estado', 'value': visita.get_estado_display()},
        {'label': 'Notas', 'value': visita.notas or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Visita Herrador - {visita.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/herrajes-avanzado/{visita.pk}/editar/',
        'delete_url': f'/herrajes-avanzado/{visita.pk}/eliminar/',
        'list_url': '/herrajes-avanzado/',
    })


@login_required
def herraje_update(request, pk):
    visita = get_object_or_404(VisitaHerrador, pk=pk)
    if request.method == 'POST':
        form = VisitaHerradorForm(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visita actualizada')
            return redirect('herraje_detail', pk=visita.pk)
    else:
        form = VisitaHerradorForm(instance=visita)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Visita de Herrador', 'cancel_url': f'/herrajes-avanzado/{visita.pk}/'})


@login_required
def herraje_delete(request, pk):
    visita = get_object_or_404(VisitaHerrador, pk=pk)
    if request.method == 'POST':
        visita.delete()
        messages.success(request, 'Visita eliminada')
        return redirect('herraje_list')
    return render(request, 'generic/delete.html', {'object': visita, 'cancel_url': f'/herrajes-avanzado/{visita.pk}/'})
