from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from propietarios.models import Propietario


@login_required
def portal_inicio(request):
    propietario = get_object_or_404(Propietario, user=request.user)
    caballos = propietario.caballos.all()
    facturas = propietario.factura_set.all()
    context = {
        'propietario': propietario,
        'caballos': caballos,
        'facturas': facturas,
    }
    return render(request, 'portal_propietario/inicio.html', context)


@login_required
def portal_caballo(request, pk):
    propietario = get_object_or_404(Propietario, user=request.user)
    caballo = get_object_or_404(propietario.caballos.all(), pk=pk)
    return render(request, 'portal_propietario/caballo.html', {'caballo': caballo})
