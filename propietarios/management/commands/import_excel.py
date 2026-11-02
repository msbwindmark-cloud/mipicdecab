from django.core.management.base import BaseCommand
import pandas as pd
from propietarios.models import Propietario
from caballos.models import Caballo
from instalaciones.models import Box


class Command(BaseCommand):
    help = 'Importar caballos y propietarios desde archivo Excel'

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='Ruta del archivo Excel')

    def handle(self, *args, **options):
        archivo = options['archivo']
        try:
            df = pd.read_excel(archivo)
            self.stdout.write(self.style.SUCCESS(f'Archivo leído: {len(df)} filas'))
            for index, row in df.iterrows():
                try:
                    # Crear o obtener propietario
                    dni = str(row.get('DNI_CIF', f'AUTO{index}'))
                    propietario, created = Propietario.objects.get_or_create(
                        dni_cif=dni,
                        defaults={
                            'nombre': str(row.get('PROPIETARIO_NOMBRE', '')),
                            'apellidos': str(row.get('PROPIETARIO_APELLIDOS', '')),
                            'telefono': str(row.get('TELEFONO', '')),
                            'email': str(row.get('EMAIL', f'auto{index}@temp.com')),
                        }
                    )
                    
                    # Crear caballo
                    nombre = str(row.get('CABALLO_NOMBRE', f'Caballo{index}'))
                    if not Caballo.objects.filter(nombre=nombre).exists():
                        Caballo.objects.create(
                            nombre=nombre,
                            propietario=propietario,
                            raza=str(row.get('RAZA', '')) if pd.notna(row.get('RAZA')) else '',
                            microchip=str(row.get('MICROCHIP', '')) if pd.notna(row.get('MICROCHIP')) else None,
                        )
                        self.stdout.write(self.style.SUCCESS(f'Creado: {nombre}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error fila {index}: {e}'))
            self.stdout.write(self.style.SUCCESS('Importación completada'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
