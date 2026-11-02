from django.contrib import admin
from .models import Conversacion, Mensaje


class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 0
    readonly_fields = ['autor', 'fecha']


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'fecha_creacion', 'ultimo_mensaje']
    filter_horizontal = ['participantes']
    inlines = [MensajeInline]


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['conversacion', 'autor', 'contenido', 'fecha', 'leido']
    list_filter = ['leido', 'fecha']
    search_fields = ['contenido', 'autor__username']
    date_hierarchy = 'fecha'
