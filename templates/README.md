# Templates Directory

Este directorio contiene todos los templates Django del proyecto SaaS multi-tenant.

## Estructura

```
templates/
├── base.html               # Template base principal
├── base_saas.html          # Base para Panel SaaS (back-office)
├── base_client.html        # Base para Panel Cliente
├── base_auth.html          # Base para autenticación
│
├── components/             # Componentes reutilizables
│   ├── header.html         # Header principal
│   ├── sidebar.html        # Sidebar de navegación
│   ├── footer.html         # Footer
│   ├── breadcrumb.html     # Breadcrumbs
│   ├── alerts.html         # Alertas/notificaciones
│   ├── modals.html         # Modales
│   └── ...                 # Otros componentes
│
├── saas/                   # Panel SaaS (back-office)
│   ├── dashboard.html      # Dashboard principal
│   ├── clients/            # Gestión de clientes
│   ├── plans/              # Planes y precios
│   ├── modules/            # Catálogo de módulos
│   ├── billing/            # Facturación
│   └── support/            # Soporte
│
├── client/                 # Panel del Cliente
│   ├── dashboard.html      # Dashboard del cliente
│   ├── users/              # Gestión de usuarios
│   ├── roles/              # Roles y permisos
│   ├── settings/           # Configuración
│   └── modules/            # Módulos contratados
│
└── auth/                   # Autenticación
    ├── login.html          # Login
    ├── register.html       # Registro
    ├── password_reset.html # Reset password
    └── ...
```

## Convenciones

### Nomenclatura
- Templates base: `base_*.html`
- Componentes: singular, descriptivo (`header.html`, `sidebar.html`)
- Vistas: plural, descriptivo (`clients/list.html`, `users/detail.html`)

### Herencia
```django
{% extends 'base_saas.html' %}  # Para panel SaaS
{% extends 'base_client.html' %} # Para panel cliente
{% extends 'base_auth.html' %}   # Para autenticación
```

### Includes
```django
{% include 'components/header.html' %}
{% include 'components/sidebar.html' %}
```

## Stack Frontend

### CSS Framework
- **Tailwind CSS v4** - Utility-first CSS framework
- **TailAdmin Pro** - Componentes premium pre-diseñados

### JavaScript
- **Alpine.js** - Framework reactivo ligero
- **HTMX** - Interacciones dinámicas sin JS pesado

### Componentes
- ApexCharts - Gráficos interactivos
- FullCalendar - Calendarios
- Flatpickr - Date pickers
- Dropzone - File uploads

## Uso de Alpine.js

```html
<!-- Ejemplo de componente con Alpine.js -->
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open">
        Contenido dinámico
    </div>
</div>
```

## Uso de HTMX

```html
<!-- Ejemplo de carga dinámica con HTMX -->
<button hx-get="/api/data" hx-target="#result" hx-swap="innerHTML">
    Cargar datos
</button>
<div id="result"></div>
```

## Dark Mode

TailAdmin incluye soporte para dark mode usando Alpine.js:

```html
<body 
    x-data="{ darkMode: false }"
    x-init="darkMode = JSON.parse(localStorage.getItem('darkMode'))"
    :class="{'dark': darkMode}">
    <!-- Contenido -->
</body>
```

## Multi-Tenant

Los templates deben ser conscientes del tenant actual:

```django
<!-- Acceso a datos del tenant -->
{{ request.tenant.name }}
{{ request.tenant.schema_name }}
```

## Notas

- Usar siempre `{% load static %}` al principio
- Componentes reutilizables en `components/`
- Mantener separación clara entre Panel SaaS y Panel Cliente
- Seguir guía de estilo de Tailwind CSS
- Preferir Alpine.js sobre jQuery para interactividad

