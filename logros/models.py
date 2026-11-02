from django.db import models
from django.contrib.auth.models import User


class Logro(models.Model):
    clave = models.CharField(max_length=60, unique=True)
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    icono = models.CharField(max_length=20, default='🏆')
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class LogroUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logros')
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE, related_name='conseguidos')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'logro')

    def __str__(self):
        return f"{self.usuario} - {self.logro}"
