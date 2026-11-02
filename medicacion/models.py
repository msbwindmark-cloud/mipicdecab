from django.db import models
from django.utils import timezone
from caballos.models import Caballo


class Medicamento(models.Model):
    TIPO_CHOICES = [
        ('ANTIBIOTICO', 'Antibiótico'),
        ('ANTIINFLAMATORIO', 'Antiinflamatorio'),
        ('ANALGESICO', 'Analgésico'),
        ('VITAMINA', 'Vitamina/Suplemento'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre


class Tratamiento(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('COMPLETADO', 'Completado'),
        ('SUSPENDIDO', 'Suspendido'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='tratamientos')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50, help_text='Ej: Cada 12 horas, 1 vez al día')
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='ACTIVO')
    motivo = models.TextField(help_text='Motivo del tratamiento')
    veterinario = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.medicamento.nombre} ({self.estado})"
    
    @property
    def activo(self):
        return self.estado == 'ACTIVO' and (self.fecha_fin is None or self.fecha_fin >= timezone.now().date())


class AdministracionMedicamento(models.Model):
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='administraciones')
    fecha = models.DateTimeField(auto_now_add=True)
    dado = models.BooleanField(default=True)
    notas = models.TextField(blank=True, null=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.tratamiento.caballo.nombre} - {self.tratamiento.medicamento.nombre} - {self.fecha}"
