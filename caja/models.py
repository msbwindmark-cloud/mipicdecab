from django.db import models


class MovimientoCaja(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('GASTO', 'Gasto'),
    ]
    CATEGORIA_CHOICES = [
        ('PUPILAJE', 'Pupilaje'),
        ('CLASES', 'Clases'),
        ('HERRAJES', 'Herrajes'),
        ('VETERINARIO', 'Veterinario'),
        ('COMPRAS', 'Compras'),
        ('OTROS', 'Otros'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=15, choices=CATEGORIA_CHOICES)
    concepto = models.CharField(max_length=255)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    forma_pago = models.CharField(max_length=20, choices=[('EFECTIVO', 'Efectivo'), ('TARJETA', 'Tarjeta'), ('TRANSFERENCIA', 'Transferencia')], default='EFECTIVO')
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.concepto} ({self.importe}€)"
