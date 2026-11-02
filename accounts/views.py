from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

from .forms import EmailAuthenticationForm, TwoFactorForm, RegistrationForm
from .models import TwoFactorCode
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from caballos.models import ControlHerraje, ControlVeterinario
from .utils import send_2fa_email


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # En desarrollo (DEBUG=True) saltamos el 2FA para comodidad
            if settings.DEBUG:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name or user.username}!')
                return redirect('dashboard')
            # Generar y enviar código 2FA
            code = str(random.randint(100000, 999999))
            TwoFactorCode.objects.create(user=user, code=code)
            send_2fa_email(user, code)
            request.session['2fa_user_id'] = user.id
            messages.success(request, 'Código de verificación enviado a tu correo')
            return redirect('verify_2fa')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = EmailAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada. Ahora inicia sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Revisa los datos del formulario.')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def verify_2fa(request):
    if not request.session.get('2fa_user_id'):
        return redirect('login')
    
    from django.contrib.auth.models import User
    user = User.objects.get(id=request.session['2fa_user_id'])
    
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            # Verificar código (últimos 10 minutos)
            ten_minutes_ago = timezone.now() - timedelta(minutes=10)
            two_fa = TwoFactorCode.objects.filter(
                user=user,
                code=code,
                used=False,
                created_at__gte=ten_minutes_ago
            ).first()
            
            if two_fa:
                two_fa.used = True
                two_fa.save()
                login(request, user)
                del request.session['2fa_user_id']
                messages.success(request, f'¡Bienvenido {user.first_name or user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Código inválido o expirado')
    else:
        form = TwoFactorForm()
    
    return render(request, 'accounts/verify_2fa.html', {'form': form, 'user': user})


@login_required
def enviar_recordatorios_view(request):
    if request.method != 'POST':
        return redirect('dashboard')
    today = timezone.now().date()
    days_ahead = 7
    enviados = 0
    # Herrajes
    herrajes = ControlHerraje.objects.filter(
        proximo_herraje__gte=today,
        proximo_herraje__lte=today + timedelta(days=days_ahead)
    ).select_related('caballo', 'caballo__propietario')
    for h in herrajes:
        try:
            subject = f'Recordatorio: Herraje próximo - {h.caballo.nombre}'
            message = f'''Hola {h.caballo.propietario.nombre},

Te recordamos que a {h.caballo.nombre} le toca herrar el día {h.proximo_herraje}.

Por favor, contacta con nosotros para confirmar cita.

Saludos,
EcuestreManager
'''
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [h.caballo.propietario.email])
            enviados += 1
        except Exception:
            pass
    # Vacunas
    vacunas = ControlVeterinario.objects.filter(
        proxima_fecha__gte=today,
        proxima_fecha__lte=today + timedelta(days=days_ahead),
        tipo='VACUNA'
    ).select_related('caballo', 'caballo__propietario')
    for v in vacunas:
        try:
            subject = f'Recordatorio: Vacuna próxima - {v.caballo.nombre}'
            message = f'''Hola {v.caballo.propietario.nombre},

Te recordamos que {v.caballo.nombre} tiene vacunación programada para el día {v.proxima_fecha}.

Por favor, contacta con nosotros para confirmar cita.

Saludos,
EcuestreManager
'''
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [v.caballo.propietario.email])
            enviados += 1
        except Exception:
            pass
    # Email de prueba si no hubo recordatorios
    if enviados == 0:
        try:
            send_mail('Prueba EcuestreManager', 'Este es un email de prueba desde tu aplicación.', settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
            enviados = 1
            messages.info(request, 'No había recordatorios próximos. Se envió un email de prueba.')
        except Exception:
            messages.warning(request, 'No se pudo enviar email de prueba.')
    else:
        messages.success(request, f'Se enviaron {enviados} recordatorios por email.')
    return redirect('dashboard')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
