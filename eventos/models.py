from django.db import models
from caballos.models import Caballo
from propietarios.models import Propietario


class Evento(models.Model):
    TIPO_CHOICES = [
        ('COMPETICION', 'Competición'),
        ('EXHIBICION', 'Exhibición'),
        ('CLINIC', 'Clinic'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    fecha = models.DateField()
    lugar = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    caballos = models.ManyToManyField(Caballo, blank=True, related_name='eventos')
    propietarios = models.ManyToManyField(Propietario, blank=True, related_name='eventos')
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha}"


class ResultadoEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='resultados')
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE)
    posicion = models.IntegerField(null=True, blank=True)
    puntuacion = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.evento.nombre}"
    
    class Meta:
        unique_together = ['evento', 'caballo']
