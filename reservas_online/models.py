from django.db import models
from django.utils import timezone
from instalaciones.models import Pista
from propietarios.models import Propietario
from caballos.models import Caballo


class ReservaOnline(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente de Confirmación'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    TIPO_CHOICES = [
        ('CLASE', 'Clase'),
        ('ENTRENAMIENTO', 'Entrenamiento'),
        ('PASEO', 'Paseo'),
        ('OTRO', 'Otro'),
    ]
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name='reservas_online')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    caballo = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    notas = models.TextField(blank=True, null=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    confirmada_por = models.CharField(max_length=100, blank=True, null=True)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha', 'hora_inicio']
    
    def __str__(self):
        return f"{self.pista.nombre} - {self.fecha} {self.hora_inicio}-{self.hora_fin} - {self.propietario}"
    
    @property
    def duracion_horas(self):
        from datetime import datetime
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        fin = datetime.combine(self.fecha, self.hora_fin)
        return (fin - inicio).total_seconds() / 3600
