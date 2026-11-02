from django.db import models
from django.utils import timezone
from caballos.models import Caballo
from propietarios.models import Propietario


class Reproduccion(models.Model):
    ESTADO_CHOICES = [
        ('CUBRICION', 'Cubrición'),
        ('GESTACION', 'Gestación'),
        ('PARTO', 'Parto'),
        ('DESTETE', 'Destete'),
        ('FINALIZADO', 'Finalizado'),
    ]
    TIPO_CHOICES = [
        ('MONTA_NATURAL', 'Monta Natural'),
        ('INSEMINACION', 'Inseminación Artificial'),
        ('TRANSFERENCIA', 'Transferencia Embrionaria'),
    ]
    yegua = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='reproducciones_yegua')
    semental = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True, related_name='reproducciones_semental')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_cubricion = models.DateField()
    fecha_parto_estimada = models.DateField(null=True, blank=True)
    fecha_parto_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='CUBRICION')
    potro = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True, related_name='nacimiento')
    veterinario = models.CharField(max_length=150, blank=True, null=True)
    coste = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_cubricion']
    
    def __str__(self):
        return f"{self.yegua.nombre} - {self.get_tipo_display()} ({self.fecha_cubricion})"
    
    @property
    def dias_gestacion(self):
        if self.fecha_parto_real:
            return (self.fecha_parto_real - self.fecha_cubricion).days
        return (timezone.now().date() - self.fecha_cubricion).days
    
    @property
    def gestacion_completada(self):
        return self.estado in ('PARTO', 'DESTETE', 'FINALIZADO')


class ControlGestacion(models.Model):
    reproduccion = models.ForeignKey(Reproduccion, on_delete=models.CASCADE, related_name='controles')
    fecha = models.DateField(auto_now_add=True)
    semana_gestacion = models.IntegerField()
    observaciones = models.TextField()
    peso_yegua = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    veterinario = models.CharField(max_length=150, blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.reproduccion.yegua.nombre} - Semana {self.semana_gestacion}"
