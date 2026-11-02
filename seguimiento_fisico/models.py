from django.db import models
from caballos.models import Caballo


class RegistroFisico(models.Model):
    CONDICION_CHOICES = [(i, f'CC {i} / 5') for i in range(1, 6)]
    MUSCULO_CHOICES = [(i, f'Tono Muscular {i} / 5') for i in range(1, 6)]
    ESTADO_CHOICES = [
        ('OPTIMO', 'Óptimo'),
        ('BUENO', 'Bueno'),
        ('MEJORABLE', 'Mejorable'),
        ('CUIDADO', 'Necesita Cuidado'),
    ]

    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='registros_fisicos')
    fecha = models.DateField()
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2)
    condicion_corporal = models.IntegerField(choices=CONDICION_CHOICES, default=3)
    tono_muscular = models.IntegerField(choices=MUSCULO_CHOICES, default=3)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='BUENO')
    observaciones = models.TextField(blank=True)
    foto = models.URLField(blank=True, null=True, help_text='URL opcional de a foto del caballo')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha', '-creado']
        verbose_name = 'Registro Físico'
        verbose_name_plural = 'Registros Físicos'

    def __str__(self):
        return f"{self.caballo.nombre} - {self.fecha} - {self.peso_kg} kg"

    @property
    def diferencia_peso(self):
        registros = list(self.caballo.registros_fisicos.order_by('fecha'))
        if not registros or registros.index(self) == 0:
            return 0
        idx = registros.index(self)
        anterior = registros[idx - 1]
        return round(float(self.peso_kg) - float(anterior.peso_kg), 2)
