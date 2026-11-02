from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Caballo
from accounts.utils import get_propietario_for_user
import qrcode
from io import BytesIO
import base64
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill


@login_required
def exportar_caballos_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Caballos"
    
    headers = ['ID', 'Nombre', 'Propietario', 'DNI/CIF', 'Microchip', 'UELN', 'Raza', 'Capa', 'Sexo', 'Box', 'Tipo Pupilaje', 'Fecha Nacimiento']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="212529", end_color="212529", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")
    
    caballos = Caballo.objects.select_related('propietario', 'box').all()
    for row_num, caballo in enumerate(caballos, 2):
        ws.cell(row=row_num, column=1, value=caballo.id)
        ws.cell(row=row_num, column=2, value=caballo.nombre)
        ws.cell(row=row_num, column=3, value=str(caballo.propietario))
        ws.cell(row=row_num, column=4, value=caballo.propietario.dni_cif)
        ws.cell(row=row_num, column=5, value=caballo.microchip or '')
        ws.cell(row=row_num, column=6, value=caballo.ueln or '')
        ws.cell(row=row_num, column=7, value=caballo.raza or '')
        ws.cell(row=row_num, column=8, value=caballo.capa or '')
        ws.cell(row=row_num, column=9, value=caballo.get_sexo_display())
        ws.cell(row=row_num, column=10, value=str(caballo.box) if caballo.box else '')
        ws.cell(row=row_num, column=11, value=caballo.get_tipo_pupilaje_display())
        ws.cell(row=row_num, column=12, value=caballo.fecha_nacimiento.strftime('%d/%m/%Y') if caballo.fecha_nacimiento else '')
    
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Listado_Caballos.xlsx'
    wb.save(response)
    return response


@login_required
def caballo_list(request):
    propietario = get_propietario_for_user(request.user)
    query = request.GET.get('q', '')
    if propietario:
        caballos = Caballo.objects.filter(propietario=propietario).select_related('propietario', 'box').order_by('-id')
    else:
        caballos = Caballo.objects.select_related('propietario', 'box').order_by('-id')
    if query:
        caballos = caballos.filter(
            Q(nombre__icontains=query) |
            Q(microchip__icontains=query) |
            Q(ueln__icontains=query) |
            Q(propietario__nombre__icontains=query) |
            Q(propietario__apellidos__icontains=query)
        )
    paginator = Paginator(caballos, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'caballos/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'caballos/list.html', {'page_obj': page_obj, 'query': query})


def caballo_detail(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    return render(request, 'caballos/detail.html', {'caballo': caballo})


def caballo_create(request):
    from .forms import CaballoForm
    if request.method == 'POST':
        form = CaballoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Caballo registrado correctamente')
            return redirect('caballo_list')
    else:
        form = CaballoForm()
    return render(request, 'caballos/form.html', {'form': form, 'title': 'Nuevo Caballo'})


def caballo_update(request, pk):
    from .forms import CaballoForm
    caballo = get_object_or_404(Caballo, pk=pk)
    if request.method == 'POST':
        form = CaballoForm(request.POST, request.FILES, instance=caballo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Caballo actualizado correctamente')
            return redirect('caballo_detail', pk=caballo.pk)
    else:
        form = CaballoForm(instance=caballo)
    return render(request, 'caballos/form.html', {'form': form, 'title': 'Editar Caballo'})


def caballo_delete(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    if request.method == 'POST':
        caballo.delete()
        messages.success(request, 'Caballo eliminado correctamente')
        return redirect('caballo_list')
    return render(request, 'caballos/delete.html', {'caballo': caballo})


@login_required
def caballo_qr(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    url = request.build_absolute_uri(reverse('caballo_detail', args=[caballo.pk]))
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    return render(request, 'caballos/qr.html', {'caballo': caballo, 'qr_code': qr_code})


@login_required
def galeria_caballo(request, pk):
    from .models import GaleriaCaballo
    caballo = get_object_or_404(Caballo, pk=pk)
    if request.method == 'POST' and request.FILES.get('imagen'):
        GaleriaCaballo.objects.create(
            caballo=caballo,
            imagen=request.FILES['imagen'],
            descripcion=request.POST.get('descripcion', '')
        )
        messages.success(request, 'Foto añadida a la galería')
        return redirect('galeria_caballo', pk=caballo.pk)
    return render(request, 'caballos/galeria.html', {'caballo': caballo})


@login_required
def ficha_clinica_pdf(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    template_path = 'caballos/ficha_clinica_pdf.html'
    context = {'caballo': caballo}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Ficha_Clinica_{caballo.nombre}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=400)
    return response


@login_required
def historial_economico(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    return render(request, 'caballos/historial_economico.html', {'caballo': caballo})


@login_required
def control_peso(request, pk):
    from .models import PesoCaballo
    caballo = get_object_or_404(Caballo, pk=pk)
    if request.method == 'POST':
        PesoCaballo.objects.create(
            caballo=caballo,
            peso=request.POST.get('peso'),
            condicion_corporal=request.POST.get('condicion_corporal', 'IDEAL'),
            notas=request.POST.get('notas', '')
        )
        messages.success(request, 'Peso registrado')
        return redirect('control_peso', pk=caballo.pk)
    pesos = caballo.pesos.all()
    return render(request, 'caballos/control_peso.html', {'caballo': caballo, 'pesos': pesos})
