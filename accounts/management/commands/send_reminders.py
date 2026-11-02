from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from caballos.models import ControlHerraje, ControlVeterinario


class Command(BaseCommand):
    help = 'Enviar recordatorios de herrajes y vacunas próximos'

    def handle(self, *args, **options):
        today = timezone.now().date()
        days_ahead = 7
        
        # Herrajes próximos
        herrajes = ControlHerraje.objects.filter(
            proximo_herraje__gte=today,
            proximo_herraje__lte=today + timedelta(days=days_ahead)
        ).select_related('caballo', 'caballo__propietario')
        
        for h in herrajes:
            try:
                subject = f'Recordatorio: Herraje próximo - {h.caballo.nombre}'
                message = f'''
Hola {h.caballo.propietario.nombre},

Te recordamos que a {h.caballo.nombre} le toca herrar el día {h.proximo_herraje}.

Por favor, contacta con nosotros para confirmar cita.

Saludos,
EcuestreManager
                '''
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [h.caballo.propietario.email])
                self.stdout.write(self.style.SUCCESS(f'Email enviado para {h.caballo.nombre}'))
            except:
                self.stdout.write(self.style.WARNING(f'No se pudo enviar email para {h.caballo.nombre}'))
        
        # Vacunas próximas
        vacunas = ControlVeterinario.objects.filter(
            proxima_fecha__gte=today,
            proxima_fecha__lte=today + timedelta(days=days_ahead),
            tipo='VACUNA'
        ).select_related('caballo', 'caballo__propietario')
        
        for v in vacunas:
            try:
                subject = f'Recordatorio: Vacuna próxima - {v.caballo.nombre}'
                message = f'''
Hola {v.caballo.propietario.nombre},

Te recordamos que {v.caballo.nombre} tiene vacunación programada para el día {v.proxima_fecha}.

Por favor, contacta con nosotros para confirmar cita.

Saludos,
EcuestreManager
                '''
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [v.caballo.propietario.email])
                self.stdout.write(self.style.SUCCESS(f'Email enviado para {v.caballo.nombre}'))
            except:
                self.stdout.write(self.style.WARNING(f'No se pudo enviar email para {v.caballo.nombre}'))
        
        self.stdout.write(self.style.SUCCESS('Recordatorios procesados'))
