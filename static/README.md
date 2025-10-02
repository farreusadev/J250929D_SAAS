# Static Files Directory

Este directorio contiene todos los archivos estáticos del proyecto (CSS, JavaScript, imágenes).

## Estructura

```
static/
├── tailadmin/          # Assets de TailAdmin Pro
│   ├── css/
│   │   ├── style.css       # Tailwind CSS v4 compilado
│   │   └── prism.css       # Syntax highlighting
│   ├── js/
│   │   └── bundle.js       # Alpine.js + componentes compilados
│   ├── images/             # Assets visuales de TailAdmin
│   │   ├── logo/           # Logos del template
│   │   ├── icons/          # Iconos
│   │   ├── brand/          # Marcas/brands
│   │   └── ...
│   └── favicon.ico
│
└── custom/             # Assets personalizados del proyecto
    ├── css/            # CSS personalizado
    └── js/             # JavaScript personalizado
```

## Uso en Templates Django

### Cargar archivos estáticos:

```django
{% load static %}

<!-- TailAdmin CSS -->
<link rel="stylesheet" href="{% static 'tailadmin/css/style.css' %}">

<!-- TailAdmin JS (Alpine.js + componentes) -->
<script src="{% static 'tailadmin/js/bundle.js' %}"></script>

<!-- Imágenes -->
<img src="{% static 'tailadmin/images/logo/logo.svg' %}" alt="Logo">
```

## Archivos Clave

### CSS
- **style.css** - Tailwind CSS v4 con tema personalizado de TailAdmin
- **prism.css** - Para syntax highlighting de código

### JavaScript
- **bundle.js** - Incluye:
  - Alpine.js v3.14.1
  - ApexCharts (gráficos)
  - Chart.js (gráficos alternativos)
  - FullCalendar (calendario)
  - Flatpickr (date picker)
  - Dropzone (file uploads)
  - Swiper (carousels)
  - JSVectorMap (mapas)

### Imágenes
- Logos del template (modo claro y oscuro)
- Iconos SVG
- Imágenes de marcas
- Assets para ejemplos

## Notas

- Los archivos en `tailadmin/` NO deben modificarse directamente
- Para personalización, usar `custom/` directory
- Los assets se compilan desde `docs/tailadmin-html-pro-2.0-main/`
- En producción, usar `python manage.py collectstatic`

