from django.db import models
from propietarios.models import Propietario


class PuntosFidelizacion(models.Model):
    propietario = models.OneToOneField(Propietario, on_delete=models.CASCADE, related_name='puntos')
    puntos_totales = models.IntegerField(default=0)
    puntos_canjeados = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    @property
    def puntos_disponibles(self):
        return self.puntos_totales - self.puntos_canjeados
    
    def __str__(self):
        return f"{self.propietario} - {self.puntos_disponibles} puntos"


class MovimientoPuntos(models.Model):
    TIPO_CHOICES = [
        ('GANADO', 'Ganado'),
        ('CANJEADO', 'Canjeado'),
        ('EXPIRADO', 'Expirado'),
    ]
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='movimientos_puntos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    puntos = models.IntegerField()
    concepto = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.propietario} - {self.tipo} {self.puntos} pts - {self.concepto}"


class Recompensa(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    puntos_necesarios = models.IntegerField()
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.puntos_necesarios} pts)"
