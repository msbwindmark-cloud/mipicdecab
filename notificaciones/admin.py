from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['destinatario', 'tipo', 'titulo', 'leida', 'fecha', 'tiempo_transcurrido']
    list_filter = ['tipo', 'leida', 'fecha']
    search_fields = ['titulo', 'mensaje', 'destinatario__username']
    date_hierarchy = 'fecha'
