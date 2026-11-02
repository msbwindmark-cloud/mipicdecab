ECUESTREMANAGER - GUÍA RÁPIDA

1. Configurar .env con tus credenciales de Gmail:
   GMAIL_USER=tu_correo@gmail.com
   GMAIL_APP_PASSWORD=tu_app_password_de_16_caracteres

2. Activar entorno virtual:
   venv\Scripts\activate

3. Migraciones (ya aplicadas):
   python manage.py migrate

4. Generar datos de prueba (64 caballos):
   python manage.py generar_datos_prueba

5. Crear superusuario si lo necesitas:
   python manage.py createsuperuser

6. Enviar recordatorios por email:
   python manage.py send_reminders

7. Importar desde Excel:
   python manage.py import_excel archivo.xlsx

8. NO ARRANCAR SERVIDOR (según pedido)

LOGIN: /accounts/login/
ADMIN: /admin/ (solo visible si eres superuser, se abre en pestaña nueva)
2FA: Se envía código por correo tras login

MÓDULOS:
- Dashboard con alertas, gráficas, caja, stock bajo
- Caballos con ficha clínica, galería, QR, semáforos
- Propietarios con CRM completo
- Facturación con PDF, presupuestos, cobros, morosos
- Clases de equitación con inscripciones
- Instalaciones con mapa visual de boxes
- Inventario con alertas de stock bajo
- Caja con ingresos/gastos y liquidación mensual
- Calendario con FullCalendar
- Configuración del Picadero para facturas profesionales
- Búsqueda global en la barra superior
- Búsqueda en tiempo real estilo AJAX
- Paginación de 5 con últimos primero
- Semáforos de salud (herraje/vacuna)
- Exportar a Excel en todos los listados
- QR por caballo
- Galería de fotos
- Facturas PDF profesionales
- Modo oscuro
- PWA instalable en móvil
- Recordatorios por email
- Presupuestos -> Factura
- Acceso por propietario (solo ve lo suyo)
- Liquidación mensual
- Enviar factura por WhatsApp
- Ficha clínica imprimible en PDF
- Historial económico por caballo
- Control de morosos
- Campanita de alertas
- Módulos nuevos con CRUD completo (Crear/Ver/Editar/Eliminar en todos):
  - Empleados, fichajes y tareas internas
  - Mensajería interna y notificaciones
  - Limpieza, mantenimiento e instalaciones
  - Seguros, transporte y veterinaria
  - Gastos, proveedores y desparasitaciones
  - Documentos, alimentación, cursos y eventos
  - Consumos, ventas, reservas y reproducción
  - Fidelización y facturación recurrente
  - Entrenamientos con calendario y seguimiento de progreso
  - Logros / gamificación con medallas y progreso
  - Informe Semanal Profesional en PDF (caja, facturación, entrenamientos, alertas)
  - Simulador de Negocio (proyección interactiva)
  - Showcase / Landing pública (`/landing/`) → página de presentación para impresionar
