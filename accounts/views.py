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
def profile(request):
    return render(request, 'accounts/profile.html')
