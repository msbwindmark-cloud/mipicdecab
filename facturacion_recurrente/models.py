from django.db import models
from django.utils import timezone
from propietarios.models import Propietario


class FacturaRecurrente(models.Model):
    FRECUENCIA_CHOICES = [
        ('MENSUAL', 'Mensual'),
        ('BIMENSUAL', 'Bimensual'),
        ('TRIMESTRAL', 'Trimestral'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
    ]
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='facturas_recurrentes')
    concepto = models.CharField(max_length=200)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    frecuencia = models.CharField(max_length=15, choices=FRECUENCIA_CHOICES)
    dia_emision = models.IntegerField(default=1, help_text='Día del mes para emitir')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    ultima_emision = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.propietario} - {self.concepto} ({self.importe}€) - {self.get_frecuencia_display()}"
    
    @property
    def proxima_emision(self):
        if not self.activa:
            return None
        from datetime import date, timedelta
        hoy = timezone.now().date()
        if self.ultima_emision:
            if self.frecuencia == 'MENSUAL':
                next_date = self.ultima_emision.replace(day=self.dia_emision) + timedelta(days=32)
                next_date = next_date.replace(day=min(self.dia_emision, 28))
            elif self.frecuencia == 'BIMENSUAL':
                next_date = self.ultima_emision + timedelta(days=60)
            elif self.frecuencia == 'TRIMESTRAL':
                next_date = self.ultima_emision + timedelta(days=90)
            elif self.frecuencia == 'SEMESTRAL':
                next_date = self.ultima_emision + timedelta(days=180)
            else:
                next_date = self.ultima_emision + timedelta(days=365)
            return next_date
        else:
            return self.fecha_inicio
