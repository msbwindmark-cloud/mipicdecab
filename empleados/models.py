from django.db import models
from django.contrib.auth.models import User


class Empleado(models.Model):
    PUESTO_CHOICES = [
        ('CUIDADOR', 'Cuidador'),
        ('INSTRUCTOR', 'Instructor'),
        ('VETERINARIO', 'Veterinario'),
        ('HERRADOR', 'Herrador'),
        ('ADMINISTRACION', 'Administración'),
        ('LIMPIEZA', 'Limpieza'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    puesto = models.CharField(max_length=15, choices=PUESTO_CHOICES)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.get_puesto_display()}"


class HorarioEmpleado(models.Model):
    DIA_CHOICES = [
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
        ('SABADO', 'Sábado'),
        ('DOMINGO', 'Domingo'),
    ]
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=10, choices=DIA_CHOICES)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    
    class Meta:
        unique_together = ['empleado', 'dia']
    
    def __str__(self):
        return f"{self.empleado.nombre} - {self.dia}: {self.hora_entrada}-{self.hora_salida}"


class Fichaje(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='fichajes')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    notas = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.empleado.nombre} - {self.tipo} - {self.fecha_hora}"
