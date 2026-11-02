from django.db import models
from caballos.models import Caballo


class Entrenamiento(models.Model):
    INTENSIDAD_CHOICES = [
        ('LEVE', 'Leve'),
        ('MODERADO', 'Moderado'),
        ('INTENSO', 'Intenso'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='entrenamientos')
    fecha = models.DateField()
    objetivo = models.CharField(max_length=255)
    ejercicios = models.TextField(blank=True, null=True)
    duracion_min = models.IntegerField(default=60)
    intensidad = models.CharField(max_length=10, choices=INTENSIDAD_CHOICES, default='MODERADO')
    completado = models.BooleanField(default=False)
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.caballo} - {self.objetivo}"
