from django.db import models
from django.utils import timezone


class Consumo(models.Model):
    TIPO_CHOICES = [
        ('AGUA', 'Agua'),
        ('ELECTRICIDAD', 'Electricidad'),
        ('GAS', 'Gas'),
        ('COMBUSTIBLE', 'Combustible'),
        ('OTRO', 'Otro'),
    ]
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    fecha = models.DateField(default=timezone.now)
    lectura_anterior = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lectura_actual = models.DecimalField(max_digits=10, decimal_places=2)
    consumo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    importe = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=150, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha} ({self.consumo})"
    
    def save(self, *args, **kwargs):
        self.consumo = self.lectura_actual - self.lectura_anterior
        super().save(*args, **kwargs)
    
    @property
    def coste_por_unidad(self):
        if self.consumo > 0:
            return round(self.importe / self.consumo, 4)
        return 0
