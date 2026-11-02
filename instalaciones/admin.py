from django.contrib import admin
from .models import Box, Pista


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['numero', 'bloque', 'estado']
    list_filter = ['estado', 'bloque']
    search_fields = ['numero']


@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'capacidad', 'disponible']
    list_filter = ['tipo', 'disponible']
