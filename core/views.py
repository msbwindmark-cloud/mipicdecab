from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from caballos.models import Caballo
from propietarios.models import Propietario
from facturacion.models import Factura


@login_required
def busqueda_global(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        caballos = Caballo.objects.filter(
            Q(nombre__icontains=query) | Q(microchip__icontains=query) | Q(ueln__icontains=query)
        )[:5]
        for c in caballos:
            resultados.append({'tipo': 'Caballo', 'nombre': c.nombre, 'url': f'/caballos/{c.pk}/'})
        
        propietarios = Propietario.objects.filter(
            Q(nombre__icontains=query) | Q(apellidos__icontains=query) | Q(dni_cif__icontains=query)
        )[:5]
        for p in propietarios:
            resultados.append({'tipo': 'Propietario', 'nombre': str(p), 'url': f'/propietarios/{p.pk}/'})
        
        facturas = Factura.objects.filter(Q(numero_factura__icontains=query))[:5]
        for f in facturas:
            resultados.append({'tipo': 'Factura', 'nombre': f.numero_factura, 'url': f'/facturacion/{f.pk}/'})
    
    return render(request, 'core/busqueda_resultados.html', {'resultados': resultados, 'query': query})
