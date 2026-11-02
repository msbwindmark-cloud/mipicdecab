from django.db import models


class ConfiguracionPicadero(models.Model):
    nombre = models.CharField(max_length=200, default='EcuestreManager')
    logo = models.ImageField(upload_to='config/', blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cif_nif = models.CharField(max_length=20, blank=True, null=True)
    web = models.URLField(blank=True, null=True)
    pie_factura = models.TextField(blank=True, null=True, help_text='Texto que aparecerá al pie de las facturas')
    
    class Meta:
        verbose_name = 'Configuración del Picadero'
        verbose_name_plural = 'Configuración del Picadero'
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionPicadero.objects.exists():
            return
        return super().save(*args, **kwargs)
