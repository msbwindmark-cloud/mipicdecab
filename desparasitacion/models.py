from django.db import models
from django.utils import timezone
from caballos.models import Caballo


class PlanDesparasitacion(models.Model):
    TIPO_CHOICES = [
        ('INTERNA', 'Desparasitación Interna'),
        ('EXTERNA', 'Desparasitación Externa'),
        ('AMBAS', 'Ambas'),
    ]
    FRECUENCIA_CHOICES = [
        ('MENSUAL', 'Mensual'),
        ('BIMENSUAL', 'Bimensual'),
        ('TRIMESTRAL', 'Trimestral'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='plan_desparasitacion')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    producto = models.CharField(max_length=150)
    frecuencia = models.CharField(max_length=15, choices=FRECUENCIA_CHOICES)
    ultima_desparasitacion = models.DateField(null=True, blank=True)
    proxima_desparasitacion = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['proxima_desparasitacion']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.get_tipo_display()} ({self.producto})"
    
    @property
    def vencida(self):
        if self.proxima_desparasitacion:
            return self.proxima_desparasitacion < timezone.now().date()
        return False
    
    @property
    def dias_para(self):
        if self.proxima_desparasitacion:
            return (self.proxima_desparasitacion - timezone.now().date()).days
        return None


class RegistroDesparasitacion(models.Model):
    plan = models.ForeignKey(PlanDesparasitacion, on_delete=models.CASCADE, related_name='registros')
    fecha = models.DateField(auto_now_add=True)
    producto_usado = models.CharField(max_length=150)
    dosis = models.CharField(max_length=50)
    coste = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    realizado_por = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.plan.caballo.nombre} - {self.fecha} - {self.producto_usado}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update plan dates
        import datetime
        self.plan.ultima_desparasitacion = self.fecha
        freq = self.plan.frecuencia
        if freq == 'MENSUAL':
            self.plan.proxima_desparasitacion = self.fecha + datetime.timedelta(days=30)
        elif freq == 'BIMENSUAL':
            self.plan.proxima_desparasitacion = self.fecha + datetime.timedelta(days=60)
        elif freq == 'TRIMESTRAL':
            self.plan.proxima_desparasitacion = self.fecha + datetime.timedelta(days=90)
        elif freq == 'SEMESTRAL':
            self.plan.proxima_desparasitacion = self.fecha + datetime.timedelta(days=180)
        elif freq == 'ANUAL':
            self.plan.proxima_desparasitacion = self.fecha + datetime.timedelta(days=365)
        self.plan.save()
