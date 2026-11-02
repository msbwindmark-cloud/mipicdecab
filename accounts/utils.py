import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from propietarios.models import Propietario


def generate_2fa_code():
    return str(random.randint(100000, 999999))


def send_2fa_email(user, code):
    subject = 'EcuestreManager - Código de verificación'
    message = f'''
Hola {user.first_name or user.username},

Tu código de verificación para acceder a EcuestreManager es:

{code}

Este código expira en 10 minutos.

Si no has intentado iniciar sesión, ignora este mensaje.
    '''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def get_user_profile(user):
    try:
        return user.profile
    except:
        return None


def is_propietario(user):
    profile = get_user_profile(user)
    return profile and profile.role == 'PROPIETARIO'


def get_propietario_for_user(user):
    profile = get_user_profile(user)
    if profile and profile.role == 'PROPIETARIO' and profile.propietario:
        return profile.propietario
    return None


def can_view_all(user):
    profile = get_user_profile(user)
    if not profile:
        return True  # superuser/staff without profile
    return profile.role in ('ADMIN', 'EMPLEADO')