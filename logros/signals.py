from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Logro


@receiver(post_migrate)
def crear_logros(sender, **kwargs):
    logros = [
        ('BIENVENIDO', 'Nuevo Alianza', 'Registro en EcuestreManager', '🐎'),
        ('CABAÑA_10', 'Cabaña Real', '10 o más caballos en el picadero', '🏰'),
        ('ENTRENAMIENTO_1', 'Primera Paso', 'Primer entrenamiento registrado', '🏇'),
        ('COBRO_CERTO', 'Cobro Certero', 'Se ha marcado una factura como pagada', '💶'),
        ('PREP_ULTRA', 'Prepárate', 'Hay un herraje próximo pendiente', '🔨'),
    ]
    for clave, titulo, descripcion, icono in logros:
        Logro.objects.get_or_create(
            clave=clave,
            defaults={'titulo': titulo, 'descripcion': descripcion, 'icono': icono, 'activo': True},
        )
