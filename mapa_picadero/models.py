from django.db import models


class ZonaPicadero(models.Model):
    TIPO_CHOICES = [
        ('BOX', 'Box / Cuadra'),
        ('PISTA', 'Pista'),
        ('MANEGE', 'Manege'),
        ('ESTABLO', 'Establo'),
        ('OTRO', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('LIBRE', 'Libre'),
        ('OCUPADO', 'Ocupado'),
        ('LIMPIEZA', 'En Limpieza'),
        ('MANTENIMIENTO', 'Mantenimiento'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='BOX')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='LIBRE')
    pos_x = models.IntegerField(default=0, help_text='Posición X en el plano (px)')
    pos_y = models.IntegerField(default=0, help_text='Posición Y en el plano (px)')
    ancho = models.IntegerField(default=80)
    alto = models.IntegerField(default=60)
    caballo = models.ForeignKey('caballos.Caballo', on_delete=models.SET_NULL, null=True, blank=True, related_name='zona_asignada')
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Zona del Picadero'
        verbose_name_plural = 'Zonas del Picadero'

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
