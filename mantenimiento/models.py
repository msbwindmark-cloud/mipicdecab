from django.db import models
from django.utils import timezone
from instalaciones.models import Box, Pista


class Mantenimiento(models.Model):
    TIPO_CHOICES = [
        ('REPARACION', 'Reparación'),
        ('REVISION', 'Revisión'),
        ('PINTURA', 'Pintura'),
        ('FONTANERIA', 'Fontanería'),
        ('ELECTRICIDAD', 'Electricidad'),
        ('OTRO', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
    ]
    instalacion_tipo = models.CharField(max_length=10, choices=[('BOX', 'Box'), ('PISTA', 'Pista'), ('OTRO', 'Otro')])
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True, blank=True)
    pista = models.ForeignKey(Pista, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha_reporte = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    coste = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    realizado_por = models.CharField(max_length=150, blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_reporte']
    
    def __str__(self):
        if self.box:
            return f"Box {self.box.numero} - {self.get_tipo_display()}"
        elif self.pista:
            return f"{self.pista.nombre} - {self.get_tipo_display()}"
        return f"{self.get_tipo_display()} - {self.descripcion[:30]}"
    
    @property
    def vencido(self):
        if self.estado == 'PENDIENTE' and self.fecha_inicio:
            return self.fecha_inicio < timezone.now().date()
        return False
