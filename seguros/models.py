from django.db import models
from django.utils import timezone
from caballos.models import Caballo


class Seguro(models.Model):
    TIPO_CHOICES = [
        ('RC', 'Responsabilidad Civil'),
        ('ACCIDENTES', 'Accidentes'),
        ('VIDA', 'Vida/Muerte'),
        ('TODO_RIESGO', 'Todo Riesgo'),
        ('OTRO', 'Otro'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='seguros')
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    compania = models.CharField(max_length=150)
    numero_poliza = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    importe = models.DecimalField(max_digits=8, decimal_places=2)
    cobertura = models.TextField(help_text='Descripción de la cobertura')
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_vencimiento']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.get_tipo_display()} ({self.compania})"
    
    @property
    def vencido(self):
        return self.fecha_vencimiento < timezone.now().date()
    
    @property
    def dias_para_vencimiento(self):
        return (self.fecha_vencimiento - timezone.now().date()).days
