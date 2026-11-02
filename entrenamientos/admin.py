from django.contrib import admin
from .models import Entrenamiento


@admin.register(Entrenamiento)
class EntrenamientoAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'fecha', 'objetivo', 'intensidad', 'completado']
    list_filter = ['intensidad', 'completado', 'fecha']
    search_fields = ['objetivo', 'ejercicios']
