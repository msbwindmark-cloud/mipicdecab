from django.contrib import admin
from .models import Logro, LogroUsuario


@admin.register(Logro)
class LogroAdmin(admin.ModelAdmin):
    list_display = ['clave', 'titulo', 'icono', 'activo']
    search_fields = ['titulo', 'clave']


@admin.register(LogroUsuario)
class LogroUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'logro', 'fecha']
    list_filter = ['logro']
