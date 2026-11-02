from django.db import models
from django.utils import timezone
from instalaciones.models import Pista
from propietarios.models import Propietario
from caballos.models import Caballo


class ReservaPista(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name='reservas')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    caballo = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.CharField(max_length=200)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha', 'hora_inicio']
    
    def __str__(self):
        return f"{self.pista.nombre} - {self.fecha} {self.hora_inicio}-{self.hora_fin} - {self.propietario}"
    
    @property
    def duracion_horas(self):
        from datetime import datetime, timedelta
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        fin = datetime.combine(self.fecha, self.hora_fin)
        return (fin - inicio).total_seconds() / 3600
