# Especificación Técnica y Funcional: EcuestreManager (SaaS para Gestión de Picaderos)

Este documento contiene la arquitectura completa para desarrollar una aplicación web moderna orientada a la gestión integral de un centro ecuestre o picadero de más de 60 caballos, reemplazando hojas de cálculo Excel por una solución en **Python (Django)**, **Bootstrap 5**, **SweetAlert2** y **Toastify/Toasts**.

---

## 1. Módulos Principales del Sistema

1. **Gestión de Caballos (Ficha TÉCNICA/CLÍNICA):**
   * Datos del caballo (Nombre, Microchip, UELN, Raza, Capa, Fecha Nacimiento, Propietario).
   * Estado de salud y registros veterinarios (Vacunas, Desparasitaciones, Odontología).
   * Herrador y herrajes (Frecuencia, última fecha, tipo de herradura).
   * Asignación de Box / Paddock y Dieta/Alimentación (tipo de pienso, tomas diarias).

2. **Propietarios y Clientes (CRM):**
   * Datos personales, contabilidad de morosidad, contratos de pupilaje.
   * Gestión de notificaciones automáticas por correo/SMS/WhatsApp.

3. **Facturación, Pagos y Pupilaje:**
   * Cuotas mensuales fijas de pupilaje.
   * Servicios extra consumidos (clases, herrajes, suplementos, transporte).
   * Generación de facturas / recibos en PDF.
   * Historial de pagos, estado de deudas (Pendiente, Pagado, Vencido).

4. **Instalaciones y Clases/Clases de Equitación:**
   * Ocupación de boxes y pistas (pista cubierta, exterior, circular).
   * Calendario de clases, instructores y asignación de caballos de escuela.

5. **Inventario y Nutrición:**
   * Stock de pienso, forraje (heno, paja) y medicamentos.
   * Alertas de stock bajo.

---

## 2. Configuración de Base de Datos (`settings.py`)

Configuración preparada con **SQLite3** para desarrollo local y comentarios de configuración para **SQL Server** usando `mssql-django` (o `django-mssql-backend`).

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ==============================================================================

# Option 1: SQLite3 (Desarrollo y Pruebas)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Option 2: Microsoft SQL Server (Producción / Entorno Corporativo)
# Para usar SQL Server instala: pip install mssql-django pyodbc
"""
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'EcuestreManagerDB',
        'USER': 'sa_ecuestre',
        'PASSWORD': 'TuPasswordSeguro123!',
        'HOST': 'localhost', # o IP del servidor SQL Server
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes',
        },
    }
}
"""
```

---

## 3. Modelo de Datos Recomendado (`models.py`)

A continuación se detalla una estructura de modelos limpia en Django para cubrir todas las necesidades operativas:

```python
from django.db import models
from django.contrib.auth.models import User

class Propietario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    dni_cif = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Box(models.Model):
    CODIGOS_ESTADO = [
        ('LIBRE', 'Libre'),
        ('OCUPADO', 'Ocupado'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
    ]
    numero = models.CharField(max_length=10, unique=True)
    bloque = models.CharField(max_length=50, blank=True, null=True) # Ej: Nave A, Paddock Exterior
    estado = models.CharField(max_length=15, choices=CODIGOS_ESTADO, default='LIBRE')

    def __str__(self):
        return f"Box {self.numero} ({self.bloque or 'General'})"

class Caballo(models.Model):
    SEXO_CHOICES = [
        ('M', 'Macho (Castrado)'),
        ('E', 'Semental'),
        ('H', 'Hembra'),
    ]
    TIPO_PUPILAJE = [
        ('COMPLETO', 'Pupilaje Completo (Box + Pienso)'),
        ('SEMI', 'Semi-pupilaje / Paddock'),
        ('ESCUELA', 'Caballo de Escuela / Propiedad del Centro'),
    ]

    nombre = models.CharField(max_length=100)
    microchip = models.CharField(max_length=50, unique=True, blank=True, null=True)
    ueln = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número UELN / Pasaporte")
    raza = models.CharField(max_length=50, blank=True, null=True)
    capa = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='M')
    
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='caballos')
    box = models.OneToOneField(Box, on_delete=models.SET_NULL, null=True, blank=True, related_name='caballo')
    tipo_pupilaje = models.CharField(max_length=20, choices=TIPO_PUPILAJE, default='COMPLETO')
    
    dieta_detalles = models.TextField(help_text="Ej: 2 kg pienso por la mañana, 1 galleta de heno por la tarde", blank=True)
    observaciones = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='caballos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class ControlVeterinario(models.Model):
    TIPO_EVENTO = [
        ('VACUNA', 'Vacunación'),
        ('DESPARASITACION', 'Desparasitación'),
        ('DENTISTA', 'Revision Dental'),
        ('OTRO', 'Consulta / Tratamiento'),
    ]
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='eventos_veterinarios')
    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO)
    fecha_realizada = models.DateField()
    proxima_fecha = models.DateField(null=True, blank=True)
    descripcion = models.TextField()
    coste = models.DecimalField(max_length=10, decimal_places=2, default=0.00)

class ControlHerraje(models.Model):
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE, related_name='herrajes')
    herrador = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField()
    proximo_herraje = models.DateField(null=True, blank=True)
    notas = models.CharField(max_length=255, blank=True, null=True)
    coste = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class Factura(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente de Pago'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    ]
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')

class ConceptoFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='conceptos')
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
```

---

## 4. Frontend y Experiencia de Usuario (UI/UX)

Para lograr una interfaz ágil sin necesidad de frameworks JS pesados (como React/Vue), utilizaremos **Bootstrap 5**, **SweetAlert2** para confirmaciones y modales interactivos, y **Toasts** para notificaciones en tiempo real tras guardar o modificar datos.

### CDN Integrados (`base.html`)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EcuestreManager - Gestión de Picaderos</title>

    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <!-- SweetAlert2 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/sweetalert2@11.7.32/dist/sweetalert2.min.css" rel="stylesheet">
</head>
<body class="bg-light">

    <!-- Toast Notification Container -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 1100;">
      <div id="liveToast" class="toast align-items-center text-bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body" id="toastMessage">
            ¡Operación realizada con éxito!
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    </div>

    <div class="container py-4">
        {% block content %}{% endblock %}
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.7.32/dist/sweetalert2.all.min.js"></script>

    <script>
      // Helper para lanzar Toast rápido
      function showToast(message, type = 'success') {
          const toastEl = document.getElementById('liveToast');
          const toastMessage = document.getElementById('toastMessage');
          
          toastEl.className = `toast align-items-center text-bg-${type} border-0`;
          toastMessage.innerText = message;
          
          const toast = new bootstrap.Toast(toastEl);
          toast.show();
      }

      // Helper para confirmación de borrado con SweetAlert2
      function registrarPagoModal(facturaId) {
          Swal.fire({
              title: '¿Confirmar cobro?',
              text: "Esta acción marcará la factura como completada.",
              icon: 'question',
              showCancelButton: true,
              confirmButtonColor: '#198754',
              cancelButtonColor: '#6c757d',
              confirmButtonText: 'Sí, registrar pago',
              cancelButtonText: 'Cancelar'
          }).then((result) => {
              if (result.isConfirmed) {
                  // Enviar petición vía AJAX o Fetch API
                  fetch(`/facturas/cobrar/${facturaId}/`, {
                      method: 'POST',
                      headers: {'X-CSRFToken': '{{ csrf_token }}'}
                  }).then(response => {
                      if(response.ok) {
                          Swal.fire('¡Cobrado!', 'El pago ha sido registrado.', 'success')
                          .then(() => location.reload());
                      }
                  });
              }
          });
      }
    </script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## 5. Hoja de Ruta para la Implementación (Roadmap)

1. **Fase 1: Configuración del proyecto Django**
   * Inicializar proyecto `django-admin startproject ecuestre_project`.
   * Crear las aplicaciones: `caballos`, `propietarios`, `facturacion`, `instalaciones`.

2. **Fase 2: Migración masiva desde Excel**
   * Crear un comando de administración (`python manage.py import_excel`) utilizando **Pandas** u **openpyxl** para volcar la lista actual de los 60+ caballos y clientes al modelo de Django sin pérdida de información.

3. **Fase 3: Desarrollo de Paneles (Dashboards)**
   * **Dashboard de Alertas:** Listar automáticamente qué caballos cumplen el ciclo de herraje (cada 6 semanas) o requieren vacunas durante el mes actual.
   * **Dashboard de Cobros:** Gráfico sencillo con Bootstrap Cards indicando el total recaudado vs. impagados.

4. **Fase 4: Despliegue**
   * Configurar **Gunicorn** / **Nginx** si se despliega en Linux o **IIS** si se usa **SQL Server** en Windows Server.