from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Curso
from propietarios.models import Propietario


@login_required
def curso_list(request):
    query = request.GET.get('q', '')
    cursos = Curso.objects.order_by('-id')
    if query:
        cursos = cursos.filter(
            Q(nombre__icontains=query) |
            Q(nivel__icontains=query) |
            Q(instructor__icontains=query)
        )
    paginator = Paginator(cursos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'cursos/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'cursos/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def curso_create(request):
    if request.method == 'POST':
        Curso.objects.create(
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
            nivel=request.POST.get('nivel'),
            instructor=request.POST.get('instructor'),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin'),
            plazas=request.POST.get('plazas', 10),
            precio=request.POST.get('precio'),
        )
        messages.success(request, 'Curso creado')
        return redirect('curso_list')
    return render(request, 'cursos/create.html', {})


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'plazas': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


@login_required
def curso_detail(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    fields = [
        {'label': 'Nombre', 'value': curso.nombre},
        {'label': 'Descripcion', 'value': curso.descripcion},
        {'label': 'Nivel', 'value': curso.get_nivel_display()},
        {'label': 'Instructor', 'value': curso.instructor},
        {'label': 'Fecha Inicio', 'value': curso.fecha_inicio},
        {'label': 'Fecha Fin', 'value': curso.fecha_fin},
        {'label': 'Plazas', 'value': curso.plazas},
        {'label': 'Precio', 'value': curso.precio},
        {'label': 'Activo', 'value': 'Si' if curso.activo else 'No'},
        {'label': 'Plazas Disponibles', 'value': curso.plazas_disponibles},
        {'label': 'Completo', 'value': 'Si' if curso.completo else 'No'},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Curso - {curso.nombre}",
        'fields': fields,
        'edit_url': f'/cursos/{curso.pk}/editar/',
        'delete_url': f'/cursos/{curso.pk}/eliminar/',
        'list_url': '/cursos/',
    })


@login_required
def curso_update(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado')
            return redirect('curso_detail', pk=curso.pk)
    else:
        form = CursoForm(instance=curso)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Curso', 'cancel_url': f'/cursos/{curso.pk}/'})


@login_required
def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado')
        return redirect('curso_list')
    return render(request, 'generic/delete.html', {'object': curso, 'cancel_url': f'/cursos/{curso.pk}/'})
