from django.db import models
from django.utils import timezone
from caballos.models import Caballo
from propietarios.models import Propietario


class Concurso(models.Model):
    NIVEL_CHOICES = [
        ('LOCAL', 'Local'),
        ('REGIONAL', 'Regional'),
        ('NACIONAL', 'Nacional'),
        ('INTERNACIONAL', 'Internacional'),
    ]
    DISCIPLINA_CHOICES = [
        ('DOMA', 'Doma Clásica'),
        ('SALTO', 'Salto de Obstáculos'),
        ('CONCURSO_COMPLETO', 'Concurso Completo'),
        ('REINING', 'Reining'),
        ('VAQUERA', 'Doma Vaquera'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=200)
    fecha = models.DateField()
    lugar = models.CharField(max_length=200)
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES)
    disciplina = models.CharField(max_length=20, choices=DISCIPLINA_CHOICES)
    organizador = models.CharField(max_length=200, blank=True, null=True)
    coste_inscripcion = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    premio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha} ({self.get_disciplina_display()})"


class ParticipacionConcurso(models.Model):
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name='participaciones')
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    jinete = models.CharField(max_length=150, blank=True, null=True)
    posicion = models.IntegerField(null=True, blank=True)
    puntuacion = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    tiempo = models.CharField(max_length=20, blank=True, null=True)
    penalizaciones = models.IntegerField(default=0)
    clasificado = models.BooleanField(default=False)
    premio_ganado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['concurso', 'caballo']
        ordering = ['posicion']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.concurso.nombre}"
    
    @property
    def ganador(self):
        return self.posicion == 1
