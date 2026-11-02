from django.db import models
from django.utils import timezone
from caballos.models import Caballo


class VisitaHerrador(models.Model):
    TIPO_CHOICES = [
        ('HERRAJE_COMPLETO', 'Herraje Completo'),
        ('RETOQUE', 'Retoque'),
        ('DESHERRAJE', 'Desherraje'),
        ('CORRECCION', 'Corrección'),
        ('OTRO', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='visitas_herrador')
    herrador = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_programada = models.DateField()
    fecha_realizada = models.DateField(null=True, blank=True)
    tipo_herradura = models.CharField(max_length=100, blank=True, null=True)
    coste = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    proximo_herraje = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    foto_antes = models.ImageField(upload_to='herrajes/', blank=True, null=True)
    foto_despues = models.ImageField(upload_to='herrajes/', blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PROGRAMADA')
    
    class Meta:
        ordering = ['-fecha_programada']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.herrador} - {self.fecha_programada}"
    
    @property
    def vencida(self):
        return self.estado == 'PROGRAMADA' and self.fecha_programada < timezone.now().date()
    
    @property
    def pendiente(self):
        return self.estado == 'PROGRAMADA' and self.fecha_programada >= timezone.now().date()


class ProgramaHerraje(models.Model):
    FRECUENCIA_CHOICES = [
        ('4_SEMANAS', '4 semanas'),
        ('5_SEMANAS', '5 semanas'),
        ('6_SEMANAS', '6 semanas'),
        ('7_SEMANAS', '7 semanas'),
        ('8_SEMANAS', '8 semanas'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='programa_herraje')
    frecuencia = models.CharField(max_length=15, choices=FRECUENCIA_CHOICES, default='6_SEMANAS')
    ultima_visita = models.DateField(null=True, blank=True)
    proxima_visita = models.DateField(null=True, blank=True)
    herrador_preferido = models.CharField(max_length=150, blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.caballo.nombre} - cada {self.get_frecuencia_display()}"
    
    @property
    def vencido(self):
        if self.proxima_visita:
            return self.proxima_visita < timezone.now().date()
        return False
