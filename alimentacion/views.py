from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.utils import timezone
from .models import PlanAlimentacion, RegistroAlimentacion
from caballos.models import Caballo


@login_required
def alimentacion_list(request):
    query = request.GET.get('q', '')
    hoy = timezone.now().date()
    registros = RegistroAlimentacion.objects.select_related('caballo').order_by('-id')
    if query:
        registros = registros.filter(
            Q(caballo__nombre__icontains=query) |
            Q(momento__icontains=query) |
            Q(notas__icontains=query)
        )
    paginator = Paginator(registros, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    caballos = Caballo.objects.select_related('propietario', 'box').all()
    registros_hoy = RegistroAlimentacion.objects.filter(fecha=hoy)
    
    if request.htmx:
        return render(request, 'alimentacion/_lista.html', {'page_obj': page_obj, 'query': query, 'caballos': caballos, 'registros_hoy': registros_hoy, 'hoy': hoy})
    return render(request, 'alimentacion/list.html', {'page_obj': page_obj, 'query': query, 'caballos': caballos, 'registros_hoy': registros_hoy, 'hoy': hoy})


@login_required
def registrar_alimentacion(request):
    if request.method == 'POST':
        caballo_id = request.POST.get('caballo')
        momento = request.POST.get('momento')
        dado = request.POST.get('dado') == 'on'
        notas = request.POST.get('notas', '')
        caballo = Caballo.objects.get(pk=caballo_id)
        RegistroAlimentacion.objects.update_or_create(
            caballo=caballo,
            fecha=timezone.now().date(),
            momento=momento,
            defaults={'dado': dado, 'notas': notas, 'usuario': request.user.username}
        )
        messages.success(request, 'Registro de alimentación guardado')
        return redirect('alimentacion_list')
    return redirect('alimentacion_list')


class RegistroAlimentacionForm(forms.ModelForm):
    class Meta:
        model = RegistroAlimentacion
        fields = '__all__'
        widgets = {
            'caballo': forms.Select(attrs={'class': 'form-control'}),
            'momento': forms.Select(attrs={'class': 'form-control'}),
            'dado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notas': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
        }


@login_required
def registro_detail(request, pk):
    registro = get_object_or_404(RegistroAlimentacion, pk=pk)
    fields = [
        {'label': 'Caballo', 'value': registro.caballo.nombre},
        {'label': 'Fecha', 'value': registro.fecha},
        {'label': 'Momento', 'value': registro.get_momento_display()},
        {'label': 'Dado', 'value': 'Si' if registro.dado else 'No'},
        {'label': 'Usuario', 'value': registro.usuario or '-'},
        {'label': 'Notas', 'value': registro.notas or '-'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Registro Alimentación - {registro.caballo.nombre}",
        'fields': fields,
        'edit_url': f'/alimentacion/{registro.pk}/editar/',
        'delete_url': f'/alimentacion/{registro.pk}/eliminar/',
        'list_url': '/alimentacion/',
    })


@login_required
def registro_update(request, pk):
    registro = get_object_or_404(RegistroAlimentacion, pk=pk)
    if request.method == 'POST':
        form = RegistroAlimentacionForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de alimentación actualizado')
            return redirect('registro_detail', pk=registro.pk)
    else:
        form = RegistroAlimentacionForm(instance=registro)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Registro de Alimentación', 'cancel_url': f'/alimentacion/{registro.pk}/'})


@login_required
def registro_delete(request, pk):
    registro = get_object_or_404(RegistroAlimentacion, pk=pk)
    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Registro de alimentación eliminado')
        return redirect('alimentacion_list')
    return render(request, 'generic/delete.html', {'object': registro, 'cancel_url': f'/alimentacion/{registro.pk}/'})
