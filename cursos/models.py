from django.db import models
from django.utils import timezone
from propietarios.models import Propietario
from caballos.models import Caballo


class Curso(models.Model):
    NIVEL_CHOICES = [
        ('INICIACION', 'Iniciación'),
        ('PRINCIPIANTE', 'Principiante'),
        ('INTERMEDIO', 'Intermedio'),
        ('AVANZADO', 'Avanzado'),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES)
    instructor = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    plazas = models.IntegerField(default=10)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_nivel_display()})"
    
    @property
    def plazas_disponibles(self):
        inscritos = self.inscripciones.filter(estado='CONFIRMADA').count()
        return self.plazas - inscritos
    
    @property
    def completo(self):
        return self.plazas_disponibles <= 0


class InscripcionCurso(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    alumno = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    caballo = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    asistencia = models.IntegerField(default=0, help_text='Número de clases asistidas')
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['curso', 'alumno']
    
    def __str__(self):
        return f"{self.alumno} - {self.curso}"
    
    @property
    def porcentaje_asistencia(self):
        total_clases = (self.curso.fecha_fin - self.curso.fecha_inicio).days // 7 + 1
        if total_clases > 0:
            return round((self.asistencia / total_clases) * 100, 1)
        return 0
