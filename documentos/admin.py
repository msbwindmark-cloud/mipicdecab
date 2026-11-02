from django.contrib import admin
from .models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'caballo', 'propietario', 'fecha_subida', 'fecha_documento']
    list_filter = ['tipo', 'fecha_subida']
    search_fields = ['titulo', 'caballo__nombre', 'propietario__nombre']
    date_hierarchy = 'fecha_subida'
