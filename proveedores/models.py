from django.db import models


class Proveedor(models.Model):
    TIPO_CHOICES = [
        ('PIENSO', 'Pienso/Alimentación'),
        ('MEDICAMENTO', 'Medicamentos'),
        ('HERRAJE', 'Herrajes'),
        ('LIMPIEZA', 'Limpieza/Mantenimiento'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    cif_nif = models.CharField(max_length=20, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class PedidoProveedor(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('RECIBIDO', 'Recibido'),
        ('CANCELADO', 'Cancelado'),
    ]
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    concepto = models.CharField(max_length=255)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_pedido']
    
    def __str__(self):
        return f"{self.proveedor.nombre} - {self.concepto} ({self.importe}€)"
