from django.contrib import admin
from .models import LimpiezaBox, ProgramaLimpieza


@admin.register(LimpiezaBox)
class LimpiezaBoxAdmin(admin.ModelAdmin):
    list_display = ['box', 'tipo', 'fecha', 'realizada_por']
    list_filter = ['tipo', 'fecha']
    search_fields = ['box__numero', 'realizada_por']
    date_hierarchy = 'fecha'


@admin.register(ProgramaLimpieza)
class ProgramaLimpiezaAdmin(admin.ModelAdmin):
    list_display = ['box', 'tipo', 'frecuencia', 'ultima_limpieza', 'proxima_limpieza', 'activo', 'vencida']
    list_filter = ['tipo', 'frecuencia', 'activo']
    search_fields = ['box__numero']
