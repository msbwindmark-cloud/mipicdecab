from django.db import models
from django.utils import timezone
from instalaciones.models import Box


class LimpiezaBox(models.Model):
    TIPO_CHOICES = [
        ('DIARIA', 'Limpieza Diaria'),
        ('PROFUNDA', 'Limpieza Profunda'),
        ('DESINFECCION', 'Desinfección'),
    ]
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='limpiezas')
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    realizada_por = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Box {self.box.numero} - {self.get_tipo_display()} - {self.fecha}"


class ProgramaLimpieza(models.Model):
    FRECUENCIA_CHOICES = [
        ('DIARIA', 'Diaria'),
        ('SEMANAL', 'Semanal'),
        ('MENSUAL', 'Mensual'),
    ]
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='programa_limpieza')
    tipo = models.CharField(max_length=15, choices=LimpiezaBox.TIPO_CHOICES)
    frecuencia = models.CharField(max_length=10, choices=FRECUENCIA_CHOICES)
    ultima_limpieza = models.DateTimeField(null=True, blank=True)
    proxima_limpieza = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Box {self.box.numero} - {self.get_tipo_display()} ({self.frecuencia})"
    
    @property
    def vencida(self):
        if self.proxima_limpieza:
            return self.proxima_limpieza < timezone.now()
        return False
