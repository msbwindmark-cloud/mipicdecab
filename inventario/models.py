from django.db import models


class Producto(models.Model):
    TIPO_CHOICES = [
        ('PIENSO', 'Pienso'),
        ('HENO', 'Heno'),
        ('PAJA', 'Paja'),
        ('MEDICAMENTO', 'Medicamento'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    unidad = models.CharField(max_length=10, default='kg')
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def stock_bajo(self):
        return self.stock_actual <= self.stock_minimo


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"
