from django.db import models
from caballos.models import Caballo


class PlanAlimentacion(models.Model):
    MOMENTO_CHOICES = [
        ('MANANA', 'Mañana'),
        ('MEDIODIA', 'Mediodía'),
        ('TARDE', 'Tarde'),
        ('NOCHE', 'Noche'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='plan_alimentacion')
    momento = models.CharField(max_length=10, choices=MOMENTO_CHOICES)
    alimento = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    unidad = models.CharField(max_length=10, default='kg')
    notas = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['momento']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.get_momento_display()}: {self.cantidad}{self.unidad} {self.alimento}"


class RegistroAlimentacion(models.Model):
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='registros_alimentacion')
    fecha = models.DateField(auto_now_add=True)
    momento = models.CharField(max_length=10, choices=PlanAlimentacion.MOMENTO_CHOICES)
    dado = models.BooleanField(default=True)
    notas = models.TextField(blank=True, null=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        unique_together = ['caballo', 'fecha', 'momento']
        ordering = ['-fecha', 'momento']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.fecha} - {self.momento}: {'Dado' if self.dado else 'No dado'}"
