from django.db import models
from django.utils import timezone
from propietarios.models import Propietario


class Encuesta(models.Model):
    TIPO_CHOICES = [
        ('SATISFACCION', 'Satisfacción General'),
        ('SERVICIO', 'Calidad del Servicio'),
        ('INSTALACIONES', 'Estado de Instalaciones'),
        ('OTRO', 'Otro'),
    ]
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return self.titulo
    
    @property
    def total_respuestas(self):
        return self.respuestas.count()


class Pregunta(models.Model):
    TIPO_CHOICES = [
        ('TEXTO', 'Texto libre'),
        ('ESCALA', 'Escala 1-5'),
        ('SI_NO', 'Sí/No'),
        ('OPCION_MULTIPLE', 'Opción múltiple'),
    ]
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.CharField(max_length=300)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    opciones = models.TextField(blank=True, null=True, help_text='Para opción múltiple, separar por comas')
    orden = models.IntegerField(default=0)
    obligatoria = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.encuesta.titulo} - {self.texto}"


class Respuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='respuestas')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['encuesta', 'propietario']
    
    def __str__(self):
        return f"{self.propietario} - {self.encuesta}"


class RespuestaPregunta(models.Model):
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name='respuestas_preguntas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta_texto = models.TextField(blank=True, null=True)
    respuesta_numero = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.pregunta.texto}: {self.respuesta_texto or self.respuesta_numero}"
