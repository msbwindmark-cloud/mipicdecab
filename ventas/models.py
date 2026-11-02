from django.db import models
from django.utils import timezone
from caballos.models import Caballo
from propietarios.models import Propietario


class VentaCaballo(models.Model):
    ESTADO_CHOICES = [
        ('EN_VENTA', 'En Venta'),
        ('RESERVADO', 'Reservado'),
        ('VENDIDO', 'Vendido'),
        ('RETIRADO', 'Retirado'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='ventas')
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_minimo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_venta = models.DateField(null=True, blank=True)
    comprador = models.ForeignKey(Propietario, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='EN_VENTA')
    descripcion = models.TextField(help_text='Descripción para la venta')
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_publicacion']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.precio_venta}€ ({self.get_estado_display()})"
    
    @property
    def dias_en_venta(self):
        if self.fecha_venta:
            return (self.fecha_venta - self.fecha_publicacion).days
        return (timezone.now().date() - self.fecha_publicacion).days
