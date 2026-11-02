from django.contrib import admin
from .models import ConfiguracionPicadero


@admin.register(ConfiguracionPicadero)
class ConfiguracionPicaderoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email', 'cif_nif']
    
    def has_add_permission(self, request):
        if ConfiguracionPicadero.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False
