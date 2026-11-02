from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('INFO', 'Información'),
        ('ALERTA', 'Alerta'),
        ('RECORDATORIO', 'Recordatorio'),
        ('URGENTE', 'Urgente'),
    ]
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='INFO')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.destinatario.username} - {self.titulo}"
    
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
