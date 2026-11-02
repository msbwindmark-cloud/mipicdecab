from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Logro, LogroUsuario
from .services import evaluar_logros


@login_required
def logro_list(request):
    logros = Logro.objects.filter(activo=True).order_by('titulo')
    conquistas = LogroUsuario.objects.filter(usuario=request.user).select_related('logro').order_by('-fecha')
    conquistados_ids = set(conquistas.values_list('logro_id', flat=True))

    logros_conquistados = [l for l in logros if l.pk in conquistados_ids]
    logros_pendientes = [l for l in logros if l.pk not in conquistados_ids]

    total_logros = logros.count()
    conquistados_count = len(logros_conquistados)
    progreso = int((conquistados_count / total_logros) * 100) if total_logros else 0
    evaluar_logros(request.user)

    context = {
        'logros_conquistados': logros_conquistados,
        'logros_pendientes': logros_pendientes,
        'conquistados_count': conquistados_count,
        'total_logros': total_logros,
        'progreso': progreso,
        'conquistas_recientes': conquistas[:5],
    }
    return render(request, 'logros/list.html', context)
