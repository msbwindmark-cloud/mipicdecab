from django.db import models
from django.contrib.auth.models import User
from propietarios.models import Propietario


class Conversacion(models.Model):
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='conversaciones_flotante')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversaciones_chat')
    activa = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-actualizado']

    def __str__(self):
        return f"Conversación {self.propietario}"



class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    autor = models.CharField(max_length=10, choices=[('PICADERO', 'Picadero'), ('CLIENTE', 'Cliente')])
    contenido = models.TextField()
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"{self.conversacion} - {self.autor}"
