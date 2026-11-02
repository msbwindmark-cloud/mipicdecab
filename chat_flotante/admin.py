from django.contrib import admin
from .models import Conversacion, Mensaje


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ['propietario', 'usuario', 'activa', 'actualizado']


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['conversacion', 'autor', 'fecha', 'leido']
    list_filter = ['autor', 'leido']
