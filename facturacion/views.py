from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.db.models import Q
from xhtml2pdf import pisa
from .models import Factura, ConceptoFactura
from propietarios.models import Propietario
from accounts.utils import get_propietario_for_user
from django.utils import timezone
from datetime import timedelta
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill


@login_required
def exportar_facturas_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Facturas"
    
    headers = ['ID', 'Nº Factura', 'Propietario', 'DNI/CIF', 'Fecha Emisión', 'Fecha Vencimiento', 'Total', 'Estado']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="dc3545", end_color="dc3545", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")
    
    facturas = Factura.objects.select_related('propietario').all()
    for row_num, f in enumerate(facturas, 2):
        ws.cell(row=row_num, column=1, value=f.id)
        ws.cell(row=row_num, column=2, value=f.numero_factura)
        ws.cell(row=row_num, column=3, value=str(f.propietario))
        ws.cell(row=row_num, column=4, value=f.propietario.dni_cif)
        ws.cell(row=row_num, column=5, value=f.fecha_emision.strftime('%d/%m/%Y'))
        ws.cell(row=row_num, column=6, value=f.fecha_vencimiento.strftime('%d/%m/%Y'))
        ws.cell(row=row_num, column=7, value=float(f.total))
        ws.cell(row=row_num, column=8, value=f.get_estado_display())
    
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
    response['Content-Disposition'] = 'attachment; filename=Listado_Facturas.xlsx'
    wb.save(response)
    return response


@login_required
def morosos(request):
    from propietarios.models import Propietario
    from django.db.models import Sum
    propietarios = Propietario.objects.all()
    morosos_list = []
    for p in propietarios:
        deuda = p.facturas.filter(estado='PENDIENTE').aggregate(total=Sum('total'))['total'] or 0
        if deuda > 0:
            morosos_list.append({'propietario': p, 'deuda': deuda})
    morosos_list.sort(key=lambda x: x['deuda'], reverse=True)
    return render(request, 'facturacion/morosos.html', {'morosos': morosos_list})


@login_required
def factura_list(request):
    propietario = get_propietario_for_user(request.user)
    query = request.GET.get('q', '')
    if propietario:
        facturas = Factura.objects.filter(propietario=propietario).select_related('propietario').order_by('-id')
    else:
        facturas = Factura.objects.select_related('propietario').order_by('-id')
    if query:
        facturas = facturas.filter(
            Q(numero_factura__icontains=query) |
            Q(propietario__nombre__icontains=query) |
            Q(propietario__apellidos__icontains=query) |
            Q(estado__icontains=query)
        )
    paginator = Paginator(facturas, request.GET.get("per_page", 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'facturacion/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'facturacion/list.html', {'page_obj': page_obj, 'query': query})


def factura_create(request):
    propietarios = Propietario.objects.filter(activo=True)
    if request.method == 'POST':
        propietario_id = request.POST.get('propietario')
        propietario = get_object_or_404(Propietario, pk=propietario_id)
        
        # Generar número de factura
        count = Factura.objects.count() + 1
        numero_factura = f"FAC-{count:06d}"
        
        factura = Factura.objects.create(
            propietario=propietario,
            numero_factura=numero_factura,
            fecha_vencimiento=timezone.now().date() + timedelta(days=30),
            estado='PENDIENTE'
        )
        
        # Añadir conceptos
        conceptos = request.POST.getlist('descripcion[]')
        cantidades = request.POST.getlist('cantidad[]')
        precios = request.POST.getlist('precio[]')
        
        total = 0
        for desc, cant, prec in zip(conceptos, cantidades, precios):
            if desc:
                precio = float(prec or 0)
                cantidad = int(cant or 1)
                ConceptoFactura.objects.create(
                    factura=factura,
                    descripcion=desc,
                    cantidad=cantidad,
                    precio_unitario=precio
                )
                total += precio * cantidad
        
        factura.total = total
        factura.save()
        messages.success(request, 'Factura creada correctamente')
        return redirect('factura_detail', pk=factura.pk)
    
    return render(request, 'facturacion/create.html', {'propietarios': propietarios})


def factura_detail(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    return render(request, 'facturacion/detail.html', {'factura': factura})


def factura_cobrar(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        factura.estado = 'PAGADO'
        factura.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


def factura_pdf(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    template_path = 'facturacion/pdf.html'
    context = {'factura': factura}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{factura.numero_factura}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=400)
    return response
