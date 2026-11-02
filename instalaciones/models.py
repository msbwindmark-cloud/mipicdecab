from django.db import models


class Box(models.Model):
    CODIGOS_ESTADO = [
        ('LIBRE', 'Libre'),
        ('OCUPADO', 'Ocupado'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
    ]
    numero = models.CharField(max_length=10, unique=True)
    bloque = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=15, choices=CODIGOS_ESTADO, default='LIBRE')

    def __str__(self):
        return f"Box {self.numero} ({self.bloque or 'General'})"


class Pista(models.Model):
    TIPO_PISTA = [
        ('CUBIERTA', 'Pista Cubierta'),
        ('EXTERIOR', 'Pista Exterior'),
        ('CIRCULAR', 'Pista Circular'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15, choices=TIPO_PISTA)
    capacidad = models.IntegerField(default=10)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
