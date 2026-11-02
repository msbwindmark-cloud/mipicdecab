# Guía de Funcionamiento - EcuestreManager

**EcuestreManager** es una aplicación web pensada para digitalizar la gestión integral de un picadero/centro ecuestre. Sustituye las hojas Excel por un sistema centralizado, claro y ágil para gestionar caballos, propietarios, facturación e instalaciones con más de 60 caballos.

## 1. Objetivo

Tener todo bajo control desde un solo sitio: fichas de caballos, seguimiento veterinario/herraje, pupilaje, facturación, ocupación de boxes y alertas de lo que está próximo a vencer.

## 2. Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| **Django 6** | Backend, lógica, modelos, rutas y autenticación |
| **SQLite** | Base de datos para desarrollo (preparado para SQL Server en producción) |
| **Bootstrap 5** | Maquetación, responsive y componentes |
| **FontAwesome 6** | Iconos |
| **SweetAlert2** | Confirmaciones, modales y acciones destructivas |
| **Toastify/Bootstrap Toasts** | Notificaciones rápidas tras guardar/modificar |

## 3. Estructura del proyecto

```text
piclproof/
├── caballos/           # Fichas, veterinario, herrajes
├── propietarios/       # Clientes/propietarios
├── facturacion/        # Facturas, conceptos, cobros
├── instalaciones/      # Boxes, pistas
├── ecuestre_project/   # Configuración, URLs, vistas globales
├── templates/          # Plantillas HTML
├── static/             # CSS/JS propios
├── media/              # Fotos de caballos
├── manage.py
└── venv/
```

## 4. Módulos y funcionamiento

### 4.1. Dashboard (`/`)

Es la pantalla principal. Te da un vistazo rápido al estado del picadero:

- **Caballos registrados** - Total de caballos dados de alta
- **Propietarios activos** - Clientes con pupilaje activo
- **Facturas pendientes** - Cobros por gestionar
- **Ocupación de boxes** - Boxes ocupados / total
- **Herrajes próximos** - Alertas de los caballos que les toca herrar
- **Vacunas/Desparasitaciones próximas** - Recordatorios veterinarios

### 4.2. Gestión de Caballos (`/caballos/`)

Aquí llevas el "historial" de cada caballo.

**Funcionalidades:**
- **Listado** con nombre, propietario, box, tipo de pupilaje y sexo
- **Alta/Edición** con todos los datos: microchip, UELN/Pasaporte, raza, capa, fecha nacimiento, sexo, propietario, box, tipo de pupilaje, dieta, observaciones, foto
- **Ficha completa** con toda su información
- **Control Veterinario** (desde admin): Vacunación, Desparasitación, Revisión dental, otros. Permite poner fecha realizada, **próxima fecha** y coste
- **Control Herraje** (desde admin): Herrador, fecha, **próximo herraje**, notas y coste

**Tipos de pupilaje:**
- `Pupilaje Completo (Box + Pienso)`
- `Semi-pupilaje / Paddock`
- `Caballo de Escuela / Propiedad del Centro`

### 4.3. Propietarios / CRM (`/propietarios/`)

Gestión de todos los clientes del picadero.

- **Ficha completa**: Nombre, apellidos, DNI/CIF, teléfono, email, dirección
- **Estado**: Activo/Inactivo
- **Relación directa** con sus caballos y facturas
- **Fecha de alta** automática

### 4.4. Facturación (`/facturacion/`)

El corazón de la parte económica.

- **Listado** con estado visual por color (Pendiente / Pagado / Cancelado)
- **Crear factura** con múltiples conceptos (pupilaje, clases, herrajes, suplementos, transporte...)
- **Detalle de factura** con desglose por líneas, cantidades, precios y total
- **Cobro rápido** con SweetAlert2 (marca la factura como PAGADA con un clic)
- **Numeración automática** (`FAC-000001`, `FAC-000002`...)
- **Fecha de vencimiento** automática (+30 días al crear)

### 4.5. Instalaciones (`/instalaciones/`)

Control visual de la infraestructura.

- **Boxes** con estado por color: `Libre` (verde), `Ocupado` (rojo), `En Mantenimiento` (amarillo). Se ve bloque/nave y número
- **Pistas**: Cubierta/Exterior/Circular, capacidad y disponibilidad

### 4.6. Módulos nuevos con CRUD completo

Desde el último refuerzo de la app, **todos los módulos nuevos** ya tienen CRUD completo (Listado + Crear + Ver + Editar + Eliminar) con paginación de 5, búsqueda en tiempo real (HTMX) y botones de acción en cada listado:

- **Empleados y Fichajes** (`/empleados/`)
- **Tareas internas** (`/tareas/`)
- **Seguros y Transporte** (`/seguros/`, `/transporte/`)
- **Mantenimiento e Instalaciones** (`/mantenimiento/`, `/instalaciones/`)
- **Limpieza de boxes** (`/limpieza/`)
- **Gastos y Proveedores** (`/gastos_caballo/`, `/proveedores/`)
- **Veterinaria** (`/medicacion/`, `/visitas_vet/`, `/desparasitacion/`)
- **Herrajes avanzados** (`/herrajes_avanzado/`)
- **Facturación** (`/facturacion/`, `/facturacion_recurrente/`)
- **Eventos y Concursos** (`/eventos/`, `/concursos/`)
- **Alimentación y Cursos** (`/alimentacion/`, `/cursos/`)
- **Encuestas, Consumos y Documentos** (`/encuestas/`, `/consumos/`, `/documentos/`)
- **Ventas y Reservas** (`/ventas/`, `/reservas/`)
- **Fidelización** (`/fidelizacion/`)
- **Reproducción** (`/reproduccion/`)
- **Entrenamientos** (`/entrenamientos/`) → con eventos en el calendario
- **Logros / Gamificación** (`/logros/`) → medallas por hitos del picadero
- **Informe Semanal Profesional en PDF** (caja, facturación, entrenamientos, alertas)
- **Simulador de Negocio** (`/reportes/simulador/`) → proyección interactiva de ingresos/gastos con gráfico
- **Showcase / Landing pública** (`/landing/`) → página de presentación con contadores animados para impresionar

Cada módulo sigue el patrón común: listado paginado (5 por página, últimos primero) con búsqueda en vivo vía HTMX, ficha de detalle con todos los datos, formulario de alta/edición y confirmación de borrado. Los listados incluyen botones **Ver / Editar / Eliminar** en cada fila.

## 5. Acceso a la aplicación

| Ruta | Acceso | Descripción |
|---|---|---|
| `/accounts/login/` | Público | Login con 2FA por Gmail (App Password) |
| `/accounts/verify-2fa/` | Público | Verificación del código de 6 dígitos |
| `/` | Privada | Dashboard con alertas, gráficas, caja, stock |
| `/admin/` | Solo staff/superuser | Administración completa de todo el sistema (abre en pestaña nueva) |
| `/caballos/` | Privada | Listado y gestión de caballos |
| `/propietarios/` | Privada | Gestión de propietarios |
| `/facturacion/` | Privada | Facturación y cobros |
| `/instalaciones/` | Privada | Estado de boxes y pistas |

**Credenciales actuales:**

```
Usuario: admin
Contraseña: admin123
```

## 6. Cómo ejecutar en local (cuando quieras)

**Importante:** No lo he arrancado tal como pediste. Si quieres probarlo en local, desde la raíz del proyecto:

```bash
# Activar venv
venv\Scripts\activate

# Migraciones (ya aplicadas)
python manage.py migrate

# Arrancar servidor
python manage.py runserver
```

Abrir: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) o [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 7. Flujo de uso recomendado

1. **Configurar instalaciones** → Ir a `/admin/instalaciones/` y dar de alta boxes y pistas
2. **Dar de alta propietarios** → `/propietarios/crear/` o desde admin
3. **Dar de alta caballos** → `/caballos/crear/` asignando propietario y box
4. **Llevar controles** → Desde admin añadir eventos veterinarios y herrajes (con `proxima_fecha` / `proximo_herraje`)
5. **Facturar** → `/facturacion/crear/` añadir conceptos y generar factura
6. **Cobrar** → Desde listado de facturas pulsar "Cobrar" o desde detalle

## 8. Estado actual vs Especificación

| Punto del documento | Estado |
|---|---|
| Modelos completos | ✅ Implementados |
| Dashboard con alertas | ✅ Implementado |
| CRUD Caballos/Propietarios | ✅ Implementado |
| Facturación con conceptos | ✅ Implementado |
| Gestión de Boxes/Pistas | ✅ Implementado |
| Plantilla base con Bootstrap + SweetAlert2 + Toasts | ✅ Implementado |
| Admin configurado | ✅ Implementado |
| Importador Excel (`import_excel`) | ⏳ Pendiente (siguiente paso) |
| Login propio + MFA | ✅ Implementado (2FA por Gmail App Password) |
| Generación PDF | ✅ Implementado (facturas, fichas) |
| CRUD completo en módulos nuevos | ✅ Implementado (todos los módulos nuevos tienen Crear/Ver/Editar/Eliminar) |

## 9. Sugerencia para "dejarla impresionada"

Mi propuesta directa y efectiva: **autenticación por roles + 2FA por email + facturas PDF + calendario + acceso por propietario**.

Con eso vas a tener una app que parece hecha para vender, no para un picadero. Limpia, práctica y con ese aire profesional que siempre impresiona.

Dime el orden que prefieras y empezamos sin perder tiempo.