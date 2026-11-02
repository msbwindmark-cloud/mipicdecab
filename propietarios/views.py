from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from .models import Propietario
from accounts.utils import get_propietario_for_user
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill


@login_required
def exportar_propietarios_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Propietarios"
    
    headers = ['ID', 'Nombre', 'Apellidos', 'DNI/CIF', 'Teléfono', 'Email', 'Dirección', 'Activo', 'Fecha Alta']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="198754", end_color="198754", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")
    
    propietarios = Propietario.objects.all()
    for row_num, p in enumerate(propietarios, 2):
        ws.cell(row=row_num, column=1, value=p.id)
        ws.cell(row=row_num, column=2, value=p.nombre)
        ws.cell(row=row_num, column=3, value=p.apellidos)
        ws.cell(row=row_num, column=4, value=p.dni_cif)
        ws.cell(row=row_num, column=5, value=p.telefono)
        ws.cell(row=row_num, column=6, value=p.email)
        ws.cell(row=row_num, column=7, value=p.direccion or '')
        ws.cell(row=row_num, column=8, value='Sí' if p.activo else 'No')
        ws.cell(row=row_num, column=9, value=p.fecha_alta.strftime('%d/%m/%Y'))
    
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        ws.column_dimensions[column_letter].width = (max_length + 2)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Listado_Propietarios.xlsx'
    wb.save(response)
    return response


@login_required
def propietario_list(request):
    propietario = get_propietario_for_user(request.user)
    query = request.GET.get('q', '')
    if propietario:
        propietarios = Propietario.objects.filter(id=propietario.id).order_by('-id')
    else:
        propietarios = Propietario.objects.order_by('-id')
    if query:
        propietarios = propietarios.filter(
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(dni_cif__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )
    paginator = Paginator(propietarios, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'propietarios/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'propietarios/list.html', {'page_obj': page_obj, 'query': query})


def propietario_detail(request, pk):
    propietario = get_object_or_404(Propietario, pk=pk)
    return render(request, 'propietarios/detail.html', {'propietario': propietario})


def propietario_create(request):
    from .forms import PropietarioForm
    if request.method == 'POST':
        form = PropietarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Propietario registrado correctamente')
            return redirect('propietario_list')
    else:
        form = PropietarioForm()
    return render(request, 'propietarios/form.html', {'form': form, 'title': 'Nuevo Propietario'})


def propietario_update(request, pk):
    from .forms import PropietarioForm
    propietario = get_object_or_404(Propietario, pk=pk)
    if request.method == 'POST':
        form = PropietarioForm(request.POST, instance=propietario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Propietario actualizado correctamente')
            return redirect('propietario_detail', pk=propietario.pk)
    else:
        form = PropietarioForm(instance=propietario)
    return render(request, 'propietarios/form.html', {'form': form, 'title': 'Editar Propietario'})
