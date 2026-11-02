from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('EMPLEADO', 'Empleado/Cuidador'),
        ('PROPIETARIO', 'Propietario'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=15, choices=ROLES, default='EMPLEADO')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    propietario = models.ForeignKey('propietarios.Propietario', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class TwoFactorCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.code}"
