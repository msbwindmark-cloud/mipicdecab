from django.db import models
from django.utils import timezone
from caballos.models import Caballo
from propietarios.models import Propietario


class Transporte(models.Model):
    TIPO_CHOICES = [
        ('COMPETICION', 'Competición'),
        ('VETERINARIO', 'Veterinario'),
        ('VENTA', 'Venta/Compra'),
        ('TRASLADO', 'Traslado'),
        ('OTRO', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('PROGRAMADO', 'Programado'),
        ('EN_CURSO', 'En Curso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='transportes')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField(null=True, blank=True)
    origen = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    transportista = models.CharField(max_length=150, blank=True, null=True)
    vehiculo = models.CharField(max_length=100, blank=True, null=True)
    coste = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PROGRAMADO')
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_salida']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.origen} → {self.destino} ({self.fecha_salida})"
    
    @property
    def duracion(self):
        if self.fecha_llegada:
            return self.fecha_llegada - self.fecha_salida
        return None
