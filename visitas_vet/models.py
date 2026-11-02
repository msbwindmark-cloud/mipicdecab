from django.db import models
from django.utils import timezone
from caballos.models import Caballo


class VisitaVeterinaria(models.Model):
    TIPO_CHOICES = [
        ('REVISION', 'Revisión General'),
        ('URGENCIA', 'Urgencia'),
        ('CIRUGIA', 'Cirugía'),
        ('SEGUIMIENTO', 'Seguimiento'),
        ('VACUNACION', 'Vacunación'),
        ('OTRO', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='visitas_veterinarias')
    veterinario = models.CharField(max_length=150)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    fecha_programada = models.DateField()
    fecha_realizada = models.DateField(null=True, blank=True)
    motivo = models.TextField()
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    coste = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PROGRAMADA')
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_programada']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.get_tipo_display()} - {self.fecha_programada}"
    
    @property
    def pendiente(self):
        return self.estado == 'PROGRAMADA' and self.fecha_programada >= timezone.now().date()
    
    @property
    def vencida(self):
        return self.estado == 'PROGRAMADA' and self.fecha_programada < timezone.now().date()
