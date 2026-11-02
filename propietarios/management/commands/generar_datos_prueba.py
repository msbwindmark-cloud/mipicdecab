from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from propietarios.models import Propietario
from caballos.models import Caballo, ControlVeterinario, ControlHerraje
from instalaciones.models import Box
from facturacion.models import Factura, ConceptoFactura
from inventario.models import Producto


class Command(BaseCommand):
    help = 'Generar datos de prueba con 64 caballos'

    def handle(self, *args, **options):
        nombres_caballos = ['Thunder', 'Luna', 'Estrella', 'Rayo', 'Viento', 'Sol', 'Nube', 'Tormenta', 'Fuego', 'Hielo', 'Diamante', 'Perla', 'Oro', 'Plata', 'Bronce', 'Cobre', 'Hierro', 'Acero', 'Titanio', 'Cromo', 'Niquel', 'Cobalto', 'Zinc', 'Plomo', 'Mercurio', 'Estaño', 'Aluminio', 'Cobre2', 'Hierro2', 'Acero2', 'Titanio2', 'Cromo2', 'Niquel2', 'Cobalto2', 'Zinc2', 'Plomo2', 'Mercurio2', 'Estaño2', 'Aluminio2', 'Cobre3', 'Hierro3', 'Acero3', 'Titanio3', 'Cromo3', 'Niquel3', 'Cobalto3', 'Zinc3', 'Plomo3', 'Mercurio3', 'Estaño3', 'Aluminio3', 'Cobre4', 'Hierro4', 'Acero4', 'Titanio4', 'Cromo4', 'Niquel4', 'Cobalto4', 'Zinc4', 'Plomo4', 'Mercurio4', 'Estaño4', 'Aluminio4', 'Cobre5']
        razas = ['Pura Raza Española', 'Hispano-Árabe', 'Árabe', 'Cuarto de Milla', 'Trotador', 'Selle Français', 'Holsteiner', 'Oldenburger']
        capas = ['Tordo', 'Castaño', 'Negro', 'Alazán', 'Bayo', 'Palomino', 'Isabelo', 'Ruano']
        nombres_personas = ['Juan', 'María', 'Pedro', 'Ana', 'Carlos', 'Laura', 'David', 'Sofía', 'Miguel', 'Carmen', 'José', 'Isabel', 'Antonio', 'Pilar', 'Francisco', 'Rosa', 'Manuel', 'Teresa', 'Luis', 'Dolores']
        apellidos = ['García', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Gómez', 'Fernández', 'Díaz', 'Moreno', 'Muñoz', 'Álvarez', 'Romero', 'Alonso', 'Gutiérrez', 'Navarro']
        
        # Crear propietarios
        propietarios = []
        for i in range(20):
            p = Propietario.objects.create(
                nombre=random.choice(nombres_personas),
                apellidos=random.choice(apellidos),
                dni_cif=f'{random.randint(10000000, 99999999)}{random.choice("TRWAGMYFPDXBNJZSQVHLCKE")}',
                telefono=f'6{random.randint(10000000, 99999999)}',
                email=f'cliente{i}@example.com',
                direccion=f'Calle {random.choice(["Mayor", "Sol", "Luna"])} {random.randint(1, 100)}',
                activo=True
            )
            propietarios.append(p)
        
        self.stdout.write(self.style.SUCCESS(f'Creados {len(propietarios)} propietarios'))
        
        # Crear boxes
        for i in range(1, 70):
            Box.objects.get_or_create(
                numero=str(i),
                defaults={'bloque': f'Nave {random.choice(["A", "B", "C"])}', 'estado': 'LIBRE'}
            )
        
        boxes = list(Box.objects.all())
        self.stdout.write(self.style.SUCCESS(f'Creados {len(boxes)} boxes'))
        
        # Crear caballos
        caballos_creados = 0
        for i in range(64):
            nombre = nombres_caballos[i] if i < len(nombres_caballos) else f'Caballo{i}'
            propietario = random.choice(propietarios)
            box = random.choice(boxes)
            
            caballo = Caballo.objects.create(
                nombre=nombre,
                propietario=propietario,
                raza=random.choice(razas),
                capa=random.choice(capas),
                fecha_nacimiento=timezone.now().date() - timedelta(days=random.randint(1000, 6000)),
                sexo=random.choice(['M', 'E', 'H']),
                microchip=f'{random.randint(100000000000000, 999999999999999)}',
                ueln=f'ES{random.randint(100000, 999999)}',
                box=box,
                tipo_pupilaje=random.choice(['COMPLETO', 'SEMI', 'ESCUELA']),
                dieta_detalles=random.choice(['2kg pienso mañana, 1kg heno tarde', '3kg pienso + suplemento', 'Paddock con heno ad libitum']),
                estado=random.choice(['ACTIVO', 'ACTIVO', 'ACTIVO', 'EN_TRATAMIENTO', 'EN_REPOSO']),
                observaciones=random.choice(['', 'Cuidado con pata delantera izquierda', 'Alérgico a ciertos medicamentos', ''])
            )
            
            box.estado = 'OCUPADO'
            box.save()
            
            # Control veterinario
            for j in range(random.randint(1, 3)):
                ControlVeterinario.objects.create(
                    caballo=caballo,
                    tipo=random.choice(['VACUNA', 'DESPARASITACION', 'DENTISTA', 'OTRO']),
                    fecha_realizada=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                    proxima_fecha=timezone.now().date() + timedelta(days=random.randint(-10, 60)),
                    descripcion=random.choice(['Vacunación anual', 'Desparasitación interna', 'Revisión dental', 'Consulta general']),
                    coste=random.choice([0, 30, 50, 80, 120])
                )
            
            # Control herraje
            for j in range(random.randint(1, 2)):
                ControlHerraje.objects.create(
                    caballo=caballo,
                    herrador=random.choice(['Juan Herrador', 'Pedro Herrajes', 'Miguel Herrador']),
                    fecha=timezone.now().date() - timedelta(days=random.randint(30, 90)),
                    proximo_herraje=timezone.now().date() + timedelta(days=random.randint(-5, 45)),
                    notas=random.choice(['', 'Herradura de hierro', 'Herradura de aluminio', 'Sin herraje posterior']),
                    coste=random.choice([40, 50, 60, 70])
                )
            
            caballos_creados += 1
        
        self.stdout.write(self.style.SUCCESS(f'Creados {caballos_creados} caballos'))
        
        # Crear facturas
        facturas_creadas = 0
        for i in range(30):
            propietario = random.choice(propietarios)
            factura = Factura.objects.create(
                propietario=propietario,
                numero_factura=f'FAC-{i+1:06d}',
                fecha_vencimiento=timezone.now().date() + timedelta(days=random.randint(15, 60)),
                estado=random.choice(['PENDIENTE', 'PENDIENTE', 'PAGADO']),
                total=0
            )
            
            total = 0
            for j in range(random.randint(1, 4)):
                cantidad = random.randint(1, 3)
                precio = random.choice([50, 100, 150, 200, 300, 500])
                ConceptoFactura.objects.create(
                    factura=factura,
                    descripcion=random.choice(['Pupilaje mensual', 'Clase de equitación', 'Herraje', 'Suplementos', 'Transporte']),
                    cantidad=cantidad,
                    precio_unitario=precio
                )
                total += cantidad * precio
            
            factura.total = total
            factura.save()
            facturas_creadas += 1
        
        self.stdout.write(self.style.SUCCESS(f'Creadas {facturas_creadas} facturas'))
        
        # Crear productos de inventario
        productos = [
            ('Pienso Premium', 'PIENSO', 500, 100, 'kg', 1.5),
            ('Heno de Alfalfa', 'HENO', 200, 50, 'kg', 0.8),
            ('Paja', 'PAJA', 150, 30, 'kg', 0.3),
            ('Desparasitante', 'MEDICAMENTO', 20, 5, 'ud', 15.0),
            ('Vacuna Tetanos', 'MEDICAMENTO', 15, 5, 'ud', 25.0),
            ('Vitaminas', 'MEDICAMENTO', 30, 10, 'ud', 12.0),
        ]
        for nombre, tipo, stock, minimo, unidad, precio in productos:
            Producto.objects.create(
                nombre=nombre,
                tipo=tipo,
                stock_actual=stock,
                stock_minimo=minimo,
                unidad=unidad,
                precio_unitario=precio
            )
        
        self.stdout.write(self.style.SUCCESS('Datos de prueba generados correctamente'))