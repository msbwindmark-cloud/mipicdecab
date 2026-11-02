from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .models import Concurso, ParticipacionConcurso
from caballos.models import Caballo
from propietarios.models import Propietario


@login_required
def concurso_list(request):
    query = request.GET.get('q', '')
    concursos = Concurso.objects.order_by('-id')
    if query:
        concursos = concursos.filter(
            Q(nombre__icontains=query) |
            Q(lugar__icontains=query) |
            Q(disciplina__icontains=query) |
            Q(nivel__icontains=query)
        )
    paginator = Paginator(concursos, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'concursos/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'concursos/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def concurso_create(request):
    if request.method == 'POST':
        Concurso.objects.create(
            nombre=request.POST.get('nombre'),
            fecha=request.POST.get('fecha'),
            lugar=request.POST.get('lugar'),
            nivel=request.POST.get('nivel'),
            disciplina=request.POST.get('disciplina'),
            organizador=request.POST.get('organizador', ''),
            coste_inscripcion=request.POST.get('coste_inscripcion', 0),
            premio=request.POST.get('premio', 0),
            notas=request.POST.get('notas', ''),
        )
        messages.success(request, 'Concurso creado')
        return redirect('concurso_list')
    return render(request, 'concursos/create.html', {})


class ConcursoForm(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'organizador': forms.TextInput(attrs={'class': 'form-control'}),
            'coste_inscripcion': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'premio': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


@login_required
def concurso_detail(request, pk):
    concurso = get_object_or_404(Concurso, pk=pk)
    fields = [
        {'label': 'Nombre', 'value': concurso.nombre},
        {'label': 'Fecha', 'value': concurso.fecha},
        {'label': 'Lugar', 'value': concurso.lugar},
        {'label': 'Nivel', 'value': concurso.get_nivel_display()},
        {'label': 'Disciplina', 'value': concurso.get_disciplina_display()},
        {'label': 'Organizador', 'value': concurso.organizador or '-'},
        {'label': 'Coste Inscripcion', 'value': concurso.coste_inscripcion},
        {'label': 'Premio', 'value': concurso.premio},
        {'label': 'Notas', 'value': concurso.notas or '-'},
        {'label': 'Participaciones', 'value': concurso.participaciones.count()},
    ]
    return render(request, 'generic/detail.html', {
        'title': f"Concurso - {concurso.nombre}",
        'fields': fields,
        'edit_url': f'/concursos/{concurso.pk}/editar/',
        'delete_url': f'/concursos/{concurso.pk}/eliminar/',
        'list_url': '/concursos/',
    })


@login_required
def concurso_update(request, pk):
    concurso = get_object_or_404(Concurso, pk=pk)
    if request.method == 'POST':
        form = ConcursoForm(request.POST, instance=concurso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Concurso actualizado')
            return redirect('concurso_detail', pk=concurso.pk)
    else:
        form = ConcursoForm(instance=concurso)
    return render(request, 'generic/form.html', {'form': form, 'title': 'Editar Concurso', 'cancel_url': f'/concursos/{concurso.pk}/'})


@login_required
def concurso_delete(request, pk):
    concurso = get_object_or_404(Concurso, pk=pk)
    if request.method == 'POST':
        concurso.delete()
        messages.success(request, 'Concurso eliminado')
        return redirect('concurso_list')
    return render(request, 'generic/delete.html', {'object': concurso, 'cancel_url': f'/concursos/{concurso.pk}/'})
