from .models import Logro, LogroUsuario
from caballos.models import Caballo, ControlHerraje
from facturacion.models import Factura
from entrenamientos.models import Entrenamiento
from django.contrib.auth.models import User


def _datos():
    return {
        'caballos': Caballo.objects.count(),
        'entrenamientos': Entrenamiento.objects.count(),
        'facturas_pagadas': Factura.objects.filter(estado='PAGADO').count(),
        'herraje_proximo': ControlHerraje.objects.filter(proximo_herraje__isnull=False).exists(),
    }


CONDICIONES = {
    'BIENVENIDO': lambda d: d['caballos'] >= 1,
    'CABAÑA_10': lambda d: d['caballos'] >= 10,
    'ENTRENAMIENTO_1': lambda d: d['entrenamientos'] >= 1,
    'COBRO_CERTO': lambda d: d['facturas_pagadas'] >= 1,
    'PREP_ULTRA': lambda d: d['herraje_proximo'],
}


def evaluar_logros(usuario):
    datos = _datos()
    creados = []
    for logro in Logro.objects.filter(activo=True).order_by('titulo'):
        cond = CONDICIONES.get(logro.clave)
        conseguido = bool(cond and cond(datos))
        if conseguido:
            if not LogroUsuario.objects.filter(usuario=usuario, logro=logro).exists():
                LogroUsuario.objects.create(usuario=usuario, logro=logro)
                creados.append(LogroUsuario.objects.get(usuario=usuario, logro=logro))
    return creados
