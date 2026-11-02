from django.db import models
from django.utils import timezone
from caballos.models import Caballo
from propietarios.models import Propietario


class Documento(models.Model):
    TIPO_CHOICES = [
        ('PASAPORTE', 'Pasaporte'),
        ('CERTIFICADO', 'Certificado'),
        ('VACUNACION', 'Cartilla de Vacunación'),
        ('SEGURO', 'Póliza de Seguro'),
        ('FACTURA', 'Factura'),
        ('CONTRATO', 'Contrato'),
        ('OTRO', 'Otro'),
    ]
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='documentos/')
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, null=True, blank=True, related_name='documentos')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, null=True, blank=True, related_name='documentos')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    fecha_documento = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    subido_por = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"
    
    @property
    def extension(self):
        import os
        return os.path.splitext(self.archivo.name)[1].lower()
