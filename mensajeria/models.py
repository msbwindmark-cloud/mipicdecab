from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversacion(models.Model):
    participantes = models.ManyToManyField(User, related_name='conversaciones')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_mensaje = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-ultimo_mensaje']
    
    def __str__(self):
        nombres = ', '.join([u.username for u in self.participantes.all()[:3]])
        return f"Conversación: {nombres}"


class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['fecha']
    
    def __str__(self):
        return f"{self.autor.username}: {self.contenido[:50]}"
    
    @property
    def tiempo_transcurrido(self):
        delta = timezone.now() - self.fecha
        if delta.days > 0:
            return f"hace {delta.days} días"
        elif delta.seconds > 3600:
            return f"hace {delta.seconds // 3600} horas"
        elif delta.seconds > 60:
            return f"hace {delta.seconds // 60} minutos"
        return "ahora mismo"
