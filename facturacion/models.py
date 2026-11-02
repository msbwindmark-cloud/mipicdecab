from django.db import models
from propietarios.models import Propietario


class Presupuesto(models.Model):
    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADO', 'Enviado'),
        ('ACEPTADO', 'Aceptado'),
        ('RECHAZADO', 'Rechazado'),
        ('FACTURADO', 'Facturado'),
    ]
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='presupuestos')
    numero_presupuesto = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField(auto_now_add=True)
    valido_hasta = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='BORRADOR')
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Presupuesto {self.numero_presupuesto} - {self.propietario}"


class ConceptoPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='conceptos')
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario


class Factura(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente de Pago'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    ]
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='facturas')
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.SET_NULL, null=True, blank=True)
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.propietario}"


class ConceptoFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='conceptos')
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
