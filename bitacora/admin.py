from django.contrib import admin
from .models import NotaBitacora


@admin.register(NotaBitacora)
class NotaBitacoraAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'hora', 'tipo', 'titulo', 'caballo', 'autor', 'importante']
    list_filter = ['tipo', 'fecha', 'importante']
    search_fields = ['titulo', 'contenido', 'caballo__nombre']
    date_hierarchy = 'fecha'
