from django.db import models
from django.utils import timezone
from propietarios.models import Propietario
from instalaciones.models import Box
from datetime import timedelta


class Caballo(models.Model):
    SEXO_CHOICES = [
        ('M', 'Macho (Castrado)'),
        ('E', 'Semental'),
        ('H', 'Hembra'),
    ]
    TIPO_PUPILAJE = [
        ('COMPLETO', 'Pupilaje Completo (Box + Pienso)'),
        ('SEMI', 'Semi-pupilaje / Paddock'),
        ('ESCUELA', 'Caballo de Escuela / Propiedad del Centro'),
    ]
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('EN_TRATAMIENTO', 'En Tratamiento'),
        ('EN_REPOSO', 'En Reposo'),
        ('VENDIDO', 'Vendido'),
        ('BAJA', 'Baja'),
    ]

    nombre = models.CharField(max_length=100)
    microchip = models.CharField(max_length=50, unique=True, blank=True, null=True)
    ueln = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número UELN / Pasaporte")
    raza = models.CharField(max_length=50, blank=True, null=True)
    capa = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='M')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='caballos')
    box = models.OneToOneField(Box, on_delete=models.SET_NULL, null=True, blank=True, related_name='caballo')
    tipo_pupilaje = models.CharField(max_length=20, choices=TIPO_PUPILAJE, default='COMPLETO')
    
    dieta_detalles = models.TextField(help_text="Ej: 2 kg pienso por la mañana, 1 galleta de heno por la tarde", blank=True)
    observaciones = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='caballos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    @property
    def proximo_herraje_fecha(self):
        ultimo = self.herrajes.filter(proximo_herraje__isnull=False).order_by('-proximo_herraje').first()
        return ultimo.proximo_herraje if ultimo else None
    
    @property
    def dias_herraje(self):
        fecha = self.proximo_herraje_fecha
        if not fecha:
            return None
        return (fecha - timezone.now().date()).days
    
    @property
    def semaforo_herraje(self):
        dias = self.dias_herraje
        if dias is None:
            return 'none'
        if dias < 0:
            return 'red'
        elif dias <= 7:
            return 'orange'
        elif dias <= 14:
            return 'yellow'
        else:
            return 'green'
    
    @property
    def proxima_vacuna_fecha(self):
        ultimo = self.eventos_veterinarios.filter(proxima_fecha__isnull=False, tipo='VACUNA').order_by('-proxima_fecha').first()
        return ultimo.proxima_fecha if ultimo else None
    
    @property
    def dias_vacuna(self):
        fecha = self.proxima_vacuna_fecha
        if not fecha:
            return None
        return (fecha - timezone.now().date()).days
    
    @property
    def semaforo_vacuna(self):
        dias = self.dias_vacuna
        if dias is None:
            return 'none'
        if dias < 0:
            return 'red'
        elif dias <= 7:
            return 'orange'
        elif dias <= 14:
            return 'yellow'
        else:
            return 'green'


class PesoCaballo(models.Model):
    CONDICION_CHOICES = [
        ('MUY_DELGADO', 'Muy Delgado'),
        ('DELGADO', 'Delgado'),
        ('IDEAL', 'Ideal'),
        ('SOBREPESO', 'Sobrepeso'),
        ('OBESO', 'Obeso'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='pesos')
    fecha = models.DateField(auto_now_add=True)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    condicion_corporal = models.CharField(max_length=15, choices=CONDICION_CHOICES, default='IDEAL')
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.peso}kg ({self.fecha})"


class GaleriaCaballo(models.Model):
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='galeria')
    imagen = models.ImageField(upload_to='caballos/galeria/')
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Foto de Galería'
        verbose_name_plural = 'Galería de Fotos'
    
    def __str__(self):
        return f"{self.caballo.nombre} - {self.descripcion or 'Foto'}"


class ControlVeterinario(models.Model):
    TIPO_EVENTO = [
        ('VACUNA', 'Vacunación'),
        ('DESPARASITACION', 'Desparasitación'),
        ('DENTISTA', 'Revision Dental'),
        ('OTRO', 'Consulta / Tratamiento'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='eventos_veterinarios')
    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO)
    fecha_realizada = models.DateField()
    proxima_fecha = models.DateField(null=True, blank=True)
    descripcion = models.TextField()
    coste = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.caballo.nombre} - {self.get_tipo_display()} ({self.fecha_realizada})"


class ControlHerraje(models.Model):
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='herrajes')
    herrador = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField()
    proximo_herraje = models.DateField(null=True, blank=True)
    notas = models.CharField(max_length=255, blank=True, null=True)
    coste = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.caballo.nombre} - Herraje {self.fecha}"
