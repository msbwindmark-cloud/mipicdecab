from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import MovimientoCaja


@login_required
def caja_list(request):
    query = request.GET.get('q', '')
    movimientos = MovimientoCaja.objects.all().order_by('-fecha')
    if query:
        movimientos = movimientos.filter(
            Q(concepto__icontains=query) |
            Q(categoria__icontains=query) |
            Q(forma_pago__icontains=query)
        )
    paginator = Paginator(movimientos, request.GET.get('per_page', 5))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.htmx:
        return render(request, 'caja/_lista.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'caja/list.html', {'page_obj': page_obj, 'query': query})


@login_required
def liquidacion_mensual(request):
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    movimientos = MovimientoCaja.objects.filter(fecha__year=year, fecha__month=month)
    ingresos = movimientos.filter(tipo='INGRESO').aggregate(total=Sum('importe'))['total'] or 0
    gastos = movimientos.filter(tipo='GASTO').aggregate(total=Sum('importe'))['total'] or 0
    saldo = ingresos - gastos
    
    por_categoria = movimientos.values('categoria', 'tipo').annotate(total=Sum('importe')).order_by('categoria')
    
    return render(request, 'caja/liquidacion.html', {
        'movimientos': movimientos,
        'ingresos': ingresos,
        'gastos': gastos,
        'saldo': saldo,
        'por_categoria': por_categoria,
        'year': year,
        'month': month,
    })
