# Estructura del Proyecto Django SaaS

## Árbol de Directorios

```
J250929D_SAAS/
├── config/                         # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py                 # Settings principal
│   ├── urls.py                     # URLs principales
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                           # Aplicaciones Django (a crear)
│   ├── core/                       # App principal
│   ├── saas_admin/                 # Panel SaaS (back-office)
│   ├── client_panel/               # Panel del cliente
│   ├── tenants/                    # Multi-tenant
│   ├── modules/                    # Catálogo de módulos
│   └── billing/                    # Facturación
│
├── static/                         # Archivos estáticos
│   ├── tailadmin/                  # Assets de TailAdmin Pro
│   │   ├── css/
│   │   │   ├── style.css           # Tailwind CSS v4 compilado
│   │   │   └── prism.css           # Syntax highlighting
│   │   ├── js/
│   │   │   └── bundle.js           # Alpine.js + componentes
│   │   ├── images/                 # Logos, iconos, assets
│   │   └── favicon.ico
│   └── custom/                     # Assets personalizados
│       ├── css/
│       └── js/
│
├── templates/                      # Templates Django
│   ├── base.html                   # Template base
│   ├── base_saas.html              # Base Panel SaaS
│   ├── base_client.html            # Base Panel Cliente
│   ├── base_auth.html              # Base Auth
│   ├── components/                 # Componentes reutilizables
│   ├── saas/                       # Templates Panel SaaS
│   ├── client/                     # Templates Panel Cliente
│   └── auth/                       # Templates autenticación
│
├── docs/                           # Documentación
│   ├── tailadmin-html-pro-2.0-main/ # Fuente TailAdmin (referencia)
│   ├── TAILWIND_INTEGRATION.md     # Doc integración Tailwind
│   └── PROJECT_STRUCTURE.md        # Este archivo
│
├── media/                          # Archivos subidos por usuarios (a crear)
├── staticfiles/                    # Static files recolectados (producción)
│
├── manage.py                       # Management script Django
├── .gitignore                      # Archivos ignorados por Git
├── .env.example                    # Variables de entorno ejemplo
├── requirements.txt                # Dependencias Python (a crear)
└── README.md                       # Documentación principal
```

## Convenciones de Nomenclatura

### Aplicaciones Django
- **snake_case** para nombres de apps: `saas_admin`, `client_panel`
- Un propósito claro por app
- Apps pequeñas y enfocadas

### Templates
- **snake_case** para archivos: `dashboard.html`, `user_list.html`
- Prefijo `base_` para templates base
- Organizar por app/módulo

### Static Files
- **kebab-case** para archivos custom: `main-style.css`
- Mantener estructura de TailAdmin intacta
- Personalización en carpeta `custom/`

### Modelos
- **PascalCase** para clases: `Client`, `UserRole`
- **snake_case** para campos: `created_at`, `is_active`

### URLs
- **kebab-case**: `/client-dashboard/`, `/user-settings/`
- RESTful cuando sea posible

## Flujo de Archivos Estáticos

### Desarrollo
```
static/
└── tailadmin/
    └── css/style.css
```
Acceso: `http://localhost:8000/static/tailadmin/css/style.css`

### Producción
```bash
python manage.py collectstatic
```
```
staticfiles/
└── tailadmin/
    └── css/style.css
```

## Multi-Tenant Architecture

```
Cliente A (tenant_a)          Cliente B (tenant_b)
├── Schema: tenant_a          ├── Schema: tenant_b
├── Usuarios                  ├── Usuarios
├── Módulos activos           ├── Módulos activos
└── Datos aislados            └── Datos aislados
```

### Public Schema
- Gestión de tenants
- Planes y precios
- Catálogo de módulos
- Panel SaaS (back-office)

### Tenant Schemas
- Usuarios del cliente
- Datos del cliente
- Configuración del cliente
- Módulos activados

## Stack Tecnológico

### Backend
- Python 3.11+
- Django 5.2
- PostgreSQL (para multi-tenant)
- Celery + Redis (jobs y cache)
- Django REST Framework

### Frontend
- Tailwind CSS v4
- Alpine.js v3.14
- HTMX
- TailAdmin Pro v2.0

### Librerías JavaScript
- ApexCharts (gráficos)
- FullCalendar (calendario)
- Flatpickr (date picker)
- Dropzone (uploads)

## Apps Django a Crear

### 1. core
- Modelos base
- Utilidades comunes
- Mixins y helpers

### 2. saas_admin
- Dashboard SaaS
- Gestión de clientes/tenants
- Planes y facturación
- Soporte

### 3. client_panel
- Dashboard del cliente
- Gestión de usuarios
- Roles y permisos
- Configuración

### 4. tenants
- Multi-tenant logic
- Gestión de schemas
- Middleware de tenant

### 5. modules
- Catálogo de módulos
- Activación/desactivación
- Configuración por módulo

### 6. billing
- Planes de pago
- Suscripciones
- Facturación
- Integraciones de pago

## Siguientes Pasos

1. ✅ Estructura de carpetas creada
2. ✅ Assets de TailAdmin copiados
3. ✅ Settings.py configurado
4. ⏳ Crear templates base
5. ⏳ Integrar HTMX
6. ⏳ Crear apps Django
7. ⏳ Implementar multi-tenant
8. ⏳ Crear modelos base

## Referencias

- [Django Best Practices](https://docs.djangoproject.com/en/5.2/)
- [Tailwind CSS v4](https://tailwindcss.com/)
- [Alpine.js](https://alpinejs.dev/)
- [HTMX](https://htmx.org/)
- [TailAdmin Pro](https://tailadmin.com/)

