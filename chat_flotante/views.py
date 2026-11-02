from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversacion, Mensaje


@login_required
def chat_panel(request):
    conversaciones = Conversacion.objects.all().select_related('propietario')
    context = {'conversaciones': conversaciones}
    return render(request, 'chat_flotante/panel.html', context)


@login_required
def chat_conversacion(request, pk):
    conversacion = get_object_or_404(Conversacion, pk=pk)
    mensajes = conversacion.mensajes.all()
    context = {'conversacion': conversacion, 'mensajes': mensajes}
    return render(request, 'chat_flotante/conversacion.html', context)


@login_required
def chat_enviar(request, pk):
    if request.method == 'POST':
        conversacion = get_object_or_404(Conversacion, pk=pk)
        contenido = request.POST.get('contenido', '')
        if contenido:
            Mensaje.objects.create(conversacion=conversacion, autor='PICADERO', contenido=contenido)
            conversacion.save()
        return redirect('chat_conversacion', pk=pk)
    return JsonResponse({'error': 'POST requerida'})
