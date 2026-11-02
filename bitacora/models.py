from django.db import models
from django.contrib.auth.models import User
from caballos.models import Caballo


class NotaBitacora(models.Model):
    TIPO_CHOICES = [
        ('GENERAL', 'General'),
        ('VETERINARIO', 'Veterinario'),
        ('HERRAJE', 'Herraje'),
        ('ALIMENTACION', 'Alimentación'),
        ('INCIDENCIA', 'Incidencia'),
        ('OTRO', 'Otro'),
    ]
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='GENERAL')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    caballo = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    importante = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha', '-hora']
    
    def __str__(self):
        return f"{self.fecha} - {self.titulo}"
