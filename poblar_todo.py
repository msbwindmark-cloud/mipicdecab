#!/usr/bin/env python
"""
poblar_todo.py
Script standalone para poblar de datos de prueba TODA la aplicacion.

Uso (desde la raiz del proyecto, con el venv activo):
    python poblar_todo.py

En otro equipo/sitio:
    1. Copia este archivo a la raiz del proyecto (junto a manage.py).
    2. Activa el venv e instala dependencias.
    3. Ejecuta: python poblar_todo.py
"""
import os
import sys
import random
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecuestre_project.settings')
django.setup()

from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

NOMBRES = ['Juan', 'Maria', 'Pedro', 'Ana', 'Carlos', 'Laura', 'David', 'Sofia', 'Miguel', 'Carmen', 'Jose', 'Isabel', 'Antonio', 'Pilar', 'Francisco', 'Rosa', 'Manuel', 'Teresa', 'Luis', 'Dolores']
APELLIDOS = ['Garcia', 'Lopez', 'Martinez', 'Sanchez', 'Perez', 'Gomez', 'Fernandez', 'Diaz', 'Moreno', 'Munoz', 'Alvarez', 'Romero', 'Alonso', 'Gutierrez', 'Navarro']
CIUDADES = ['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'Zaragoza', 'Malaga', 'Murcia', 'Palma', 'Bilbao', 'Alicante']
RAZAS = ['Pura Raza Espanola', 'Hispano-Arabe', 'Arabe', 'Cuarto de Milla', 'Trotador', 'Selle Francais', 'Holsteiner', 'Oldenburger']
CAPAS = ['Tordo', 'Castano', 'Negro', 'Alazan', 'Bayo', 'Palomino', 'Isabelo', 'Ruano']

def make_value(field, instance_cache):
    from django.db import models
    if field.has_default():
        d = field.default
        return d() if callable(d) else d
    if getattr(field, 'null', False) and random.random() < 0.15:
        return None
    choices = getattr(field, 'choices', None)
    if choices:
        return random.choice([c[0] for c in choices])
    if isinstance(field, (models.ForeignKey, models.OneToOneField)):
        rel = field.related_model
        qs = list(rel.objects.all())
        if qs:
            return random.choice(qs)
        try:
            obj = create_one(rel, instance_cache)
            return obj
        except Exception:
            return None
    if isinstance(field, models.BooleanField):
        return random.choice([True, False])
    if isinstance(field, (models.IntegerField, models.SmallIntegerField, models.BigIntegerField, models.PositiveIntegerField)):
        return random.randint(0, 100)
    if isinstance(field, (models.DecimalField, models.FloatField)):
        return round(random.uniform(0, 500), 2)
    if isinstance(field, models.DateField):
        return (timezone.now().date() - timedelta(days=random.randint(0, 730)))
    if isinstance(field, models.DateTimeField):
        return timezone.now() - timedelta(days=random.randint(0, 730))
    if isinstance(field, models.TimeField):
        return timezone.now().time()
    if isinstance(field, models.EmailField):
        return f'user{random.randint(1,9999)}@example.com'
    if isinstance(field, models.URLField):
        return 'https://example.com'
    if isinstance(field, models.SlugField):
        return f'slug-{random.randint(1,9999)}'
    if isinstance(field, models.CharField):
        name = field.name.lower()
        if 'nombre' in name:
            return random.choice(NOMBRES)
        if 'apellido' in name:
            return random.choice(APELLIDOS)
        if 'ciudad' in name or 'localidad' in name:
            return random.choice(CIUDADES)
        if 'telefono' in name or 'tlf' in name:
            return f'6{random.randint(10000000, 99999999)}'
        if 'dni' in name or 'cif' in name:
            return f'{random.randint(10000000, 99999999)}{random.choice("TRWAGMYFPDXBNJZSQVHLCKE")}'
        if 'email' in name or 'correo' in name:
            return f'cliente{random.randint(1,9999)}@example.com'
        if 'numero' in name or 'num' in name:
            return str(random.randint(1, 999))
        if 'raza' in name:
            return random.choice(RAZAS)
        if 'capa' in name:
            return random.choice(CAPAS)
        if 'microchip' in name:
            return str(random.randint(10**14, 10**15 - 1))
        return f'texto{random.randint(1,999)}'
    if isinstance(field, models.TextField):
        return random.choice(['', 'Observacion de prueba', 'Nota generada automaticamente', 'Sin comentarios'])
    if isinstance(field, models.JSONField):
        return {}
    if isinstance(field, (models.FileField, models.ImageField)):
        return None
    return None

def create_one(model, instance_cache, attempts=3):
    last_err = None
    for _ in range(attempts):
        kwargs = {}
        m2m_fields = []
        ok = True
        try:
            for field in model._meta.get_fields():
                if field.auto_created or field.primary_key:
                    continue
                if field.many_to_many or field.one_to_many:
                    m2m_fields.append(field)
                    continue
                if getattr(field, 'name', None) is None:
                    continue
                if not getattr(field, 'editable', True):
                    continue
                val = make_value(field, instance_cache)
                if val is None and not getattr(field, 'null', False) and not field.has_default():
                    if isinstance(field, __import__('django.db.models', fromlist=['CharField']).CharField):
                        val = ''
                    else:
                        ok = False
                        break
                kwargs[field.name] = val
        except Exception as e:
            last_err = e
            ok = False
        if not ok:
            continue
        try:
            obj = model.objects.create(**kwargs)
            for mf in m2m_fields:
                rel = mf.related_model
                qs = list(rel.objects.all())
                if qs:
                    sample = random.sample(qs, min(3, len(qs)))
                    getattr(obj, mf.name).set(sample)
            instance_cache.setdefault(model, []).append(obj)
            return obj
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f'No se pudo crear {model.__name__}: {last_err}')

def ensure_user():
    if not User.objects.exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Creado superusuario admin / admin123')

def specific_seed():
    from propietarios.models import Propietario
    from caballos.models import Caballo, ControlVeterinario, ControlHerraje
    from instalaciones.models import Box
    from facturacion.models import Factura, ConceptoFactura
    from inventario.models import Producto
    if Propietario.objects.exists():
        print('Propietarios ya existen, saltando seed especifico.')
        return
    propietarios = []
    for i in range(20):
        p = Propietario.objects.create(
            nombre=random.choice(NOMBRES),
            apellidos=random.choice(APELLIDOS),
            dni_cif=f'{random.randint(10000000, 99999999)}{random.choice("TRWAGMYFPDXBNJZSQVHLCKE")}',
            telefono=f'6{random.randint(10000000, 99999999)}',
            email=f'cliente{i}@example.com',
            direccion=f'Calle {random.choice(["Mayor", "Sol", "Luna"])} {random.randint(1, 100)}',
            activo=True,
        )
        propietarios.append(p)
    print(f'Creados {len(propietarios)} propietarios')
    for i in range(1, 70):
        Box.objects.get_or_create(numero=str(i), defaults={'bloque': f'Nave {random.choice(["A", "B", "C"])}', 'estado': 'LIBRE'})
    boxes = list(Box.objects.all())
    print(f'Creados {len(boxes)} boxes')
    caballos_creados = 0
    random.shuffle(boxes)
    for i in range(64):
        nombre = f'Caballo{i+1}'
        propietario = random.choice(propietarios)
        box = boxes[i] if i < len(boxes) else None
        caballo = Caballo.objects.create(
            nombre=nombre,
            propietario=propietario,
            raza=random.choice(RAZAS),
            capa=random.choice(CAPAS),
            fecha_nacimiento=timezone.now().date() - timedelta(days=random.randint(1000, 6000)),
            sexo=random.choice(['M', 'E', 'H']),
            microchip=str(random.randint(10**14, 10**15 - 1)),
            ueln=f'ES{random.randint(100000, 999999)}',
            box=box,
            tipo_pupilaje=random.choice(['COMPLETO', 'SEMI', 'ESCUELA']),
            dieta_detalles=random.choice(['2kg pienso manana, 1kg heno tarde', '3kg pienso + suplemento', 'Paddock con heno ad libitum']),
            estado=random.choice(['ACTIVO', 'ACTIVO', 'ACTIVO', 'EN_TRATAMIENTO', 'EN_REPOSO']),
            observaciones=random.choice(['', 'Cuidado con pata delantera izquierda', 'Alergico a ciertos medicamentos', '']),
        )
        if box:
            box.estado = 'OCUPADO'
            box.save()
        for j in range(random.randint(1, 3)):
            ControlVeterinario.objects.create(
                caballo=caballo,
                tipo=random.choice(['VACUNA', 'DESPARASITACION', 'DENTISTA', 'OTRO']),
                fecha_realizada=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                proxima_fecha=timezone.now().date() + timedelta(days=random.randint(-10, 60)),
                descripcion=random.choice(['Vacunacion anual', 'Desparasitacion interna', 'Revision dental', 'Consulta general']),
                coste=random.choice([0, 30, 50, 80, 120]),
            )
        for j in range(random.randint(1, 2)):
            ControlHerraje.objects.create(
                caballo=caballo,
                herrador=random.choice(['Juan Herrador', 'Pedro Herrajes', 'Miguel Herrador']),
                fecha=timezone.now().date() - timedelta(days=random.randint(30, 90)),
                proximo_herraje=timezone.now().date() + timedelta(days=random.randint(-5, 45)),
                notas=random.choice(['', 'Herradura de hierro', 'Herradura de aluminio', 'Sin herraje posterior']),
                coste=random.choice([40, 50, 60, 70]),
            )
        caballos_creados += 1
    print(f'Creados {caballos_creados} caballos')
    facturas_creadas = 0
    for i in range(30):
        propietario = random.choice(propietarios)
        factura = Factura.objects.create(
            propietario=propietario,
            numero_factura=f'FAC-{i+1:06d}',
            fecha_vencimiento=timezone.now().date() + timedelta(days=random.randint(15, 60)),
            estado=random.choice(['PENDIENTE', 'PENDIENTE', 'PAGADO']),
            total=0,
        )
        total = 0
        for j in range(random.randint(1, 4)):
            cantidad = random.randint(1, 3)
            precio = random.choice([50, 100, 150, 200, 300, 500])
            ConceptoFactura.objects.create(
                factura=factura,
                descripcion=random.choice(['Pupilaje mensual', 'Clase de equitacion', 'Herraje', 'Suplementos', 'Transporte']),
                cantidad=cantidad,
                precio_unitario=precio,
            )
            total += cantidad * precio
        factura.total = total
        factura.save()
        facturas_creadas += 1
    print(f'Creadas {facturas_creadas} facturas')
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
            nombre=nombre, tipo=tipo, stock_actual=stock, stock_minimo=minimo,
            unidad=unidad, precio_unitario=precio,
        )
    print('Productos de inventario creados')

def generic_seed():
    from django.apps import apps as django_apps
    skip_apps = {'admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'livereload'}
    local_apps = []
    for cfg in django_apps.get_app_configs():
        if cfg.label in skip_apps:
            continue
        if not os.path.abspath(cfg.path).startswith(BASE_DIR):
            continue
        if not getattr(cfg, 'models', None):
            continue
        local_apps.append(cfg)
    instance_cache = {}
    all_models = []
    for cfg in local_apps:
        for model in cfg.get_models():
            fk_count = sum(1 for f in model._meta.get_fields()
                           if f.__class__.__name__ in ('ForeignKey', 'OneToOneField') and not f.auto_created)
            all_models.append((fk_count, model))
    all_models.sort(key=lambda x: x[0])
    for fk_count, model in all_models:
        try:
            existing = model.objects.count()
        except Exception:
            continue
        desired = 8
        if existing >= desired:
            continue
        to_create = desired - existing
        created = 0
        for _ in range(to_create):
            try:
                create_one(model, instance_cache)
                created += 1
            except Exception:
                pass
        if created:
            print(f'  {model._meta.app_label}.{model.__name__}: +{created}')

def main():
    random.seed(42)
    print('=== Poblando base de datos ===')
    ensure_user()
    specific_seed()
    print('=== Poblando resto de modelos ===')
    generic_seed()
    print('=== LISTO ===')

if __name__ == '__main__':
    main()
PY