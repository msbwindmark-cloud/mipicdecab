from django.db import models
from django.utils import timezone
from caballos.models import Caballo


class GastoCaballo(models.Model):
    CATEGORIA_CHOICES = [
        ('VETERINARIO', 'Veterinario'),
        ('HERRAJE', 'Herraje'),
        ('ALIMENTACION', 'Alimentación'),
        ('MEDICACION', 'Medicación'),
        ('TRANSPORTE', 'Transporte'),
        ('COMPETICION', 'Competición'),
        ('OTRO', 'Otro'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='gastos')
    categoria = models.CharField(max_length=15, choices=CATEGORIA_CHOICES)
    concepto = models.CharField(max_length=255)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    proveedor = models.CharField(max_length=150, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.concepto} ({self.importe}€)"
    
    @property
    def total_gastos_caballo(self):
        from django.db.models import Sum
        return GastoCaballo.objects.filter(caballo=self.caballo).aggregate(total=Sum('importe'))['total'] or 0
