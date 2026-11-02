from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.utils import get_propietario_for_user
from propietarios.models import Propietario


@login_required
def portal_inicio(request):
    propietario = get_propietario_for_user(request.user)
    if not propietario:
        messages.info(request, 'Tu usuario no está vinculado a un propietario. Contacta con el administrador.')
        return redirect('dashboard')
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
