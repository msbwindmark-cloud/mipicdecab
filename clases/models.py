from django.db import models
from caballos.models import Caballo
from propietarios.models import Propietario
from instalaciones.models import Pista


class Instructor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Clase(models.Model):
    NIVEL_CHOICES = [
        ('INICIACION', 'Iniciación'),
        ('PRINCIPIANTE', 'Principiante'),
        ('INTERMEDIO', 'Intermedio'),
        ('AVANZADO', 'Avanzado'),
    ]
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES)
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    plazas = models.IntegerField(default=8)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Clase {self.fecha} {self.hora_inicio} - {self.instructor}"


class InscripcionClase(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('ASISTIO', 'Asistió'),
    ]
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='inscripciones')
    alumno = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    caballo = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    def __str__(self):
        return f"{self.alumno} - {self.clase}"
