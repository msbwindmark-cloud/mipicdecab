from django.db import models
from django.utils import timezone
from caballos.models import Caballo
from propietarios.models import Propietario


class Residencia(models.Model):
    TIPO_CHOICES = [
        ('PUPILAJE_COMPLETO', 'Pupilaje Completo'),
        ('SEMI_PUPILAJE', 'Semi-pupilaje'),
        ('PENSION', 'Pensión'),
        ('ENTRENAMIENTO', 'Entrenamiento'),
        ('REHABILITACION', 'Rehabilitación'),
        ('OTRO', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('FINALIZADA', 'Finalizada'),
        ('SUSPENDIDA', 'Suspendida'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='residencias')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    tarifa_mensual = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='ACTIVA')
    box = models.ForeignKey('instalaciones.Box', on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.get_tipo_display()} ({self.estado})"
    
    @property
    def dias_residencia(self):
        if self.fecha_fin:
            return (self.fecha_fin - self.fecha_inicio).days
        return (timezone.now().date() - self.fecha_inicio).days
    
    @property
    def coste_total(self):
        meses = self.dias_residencia / 30
        return round(self.tarifa_mensual * meses, 2)
    
    @property
    def activa(self):
        return self.estado == 'ACTIVA'
