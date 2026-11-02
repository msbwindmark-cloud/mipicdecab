from django.contrib import admin
from .models import Caballo, ControlVeterinario, ControlHerraje, GaleriaCaballo


class GaleriaCaballoInline(admin.TabularInline):
    model = GaleriaCaballo
    extra = 1


@admin.register(Caballo)
class CaballoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'propietario', 'box', 'tipo_pupilaje', 'sexo', 'microchip']
    search_fields = ['nombre', 'microchip', 'ueln', 'propietario__nombre', 'propietario__apellidos']
    list_filter = ['tipo_pupilaje', 'sexo']
    inlines = [GaleriaCaballoInline]


@admin.register(ControlVeterinario)
class ControlVeterinarioAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'tipo', 'fecha_realizada', 'proxima_fecha', 'coste']
    list_filter = ['tipo', 'fecha_realizada']
    search_fields = ['caballo__nombre']


@admin.register(ControlHerraje)
class ControlHerrajeAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'herrador', 'fecha', 'proximo_herraje', 'coste']
    list_filter = ['herrador', 'fecha']
    search_fields = ['caballo__nombre']


@admin.register(GaleriaCaballo)
class GaleriaCaballoAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'descripcion', 'fecha']
    list_filter = ['fecha']
    search_fields = ['caballo__nombre']
