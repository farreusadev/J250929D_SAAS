# J250929D_SAAS

Plataforma SaaS Multi-Tenant construida con Django + TailAdmin Pro + HTMX + Alpine.js

## 🚀 Stack Tecnológico

### Backend
- **Python 3.11+**
- **Django 5.2** - Framework web
- **PostgreSQL** - Base de datos (multi-tenant)
- **Celery + Redis** - Jobs en background y cache
- **Django REST Framework** - API REST

### Frontend
- **Tailwind CSS v4.0** - Framework CSS utility-first
- **Alpine.js v3.14** - Framework JS reactivo ligero
- **HTMX v1.9.10** - Interacciones AJAX sin JavaScript
- **TailAdmin Pro v2.0** - Componentes UI premium

## 📁 Estructura del Proyecto

```
J250929D_SAAS/
├── config/                     # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/                     # Archivos estáticos
│   ├── tailadmin/              # Assets de TailAdmin Pro
│   │   ├── css/
│   │   │   ├── style.css       # Tailwind CSS compilado
│   │   │   └── prism.css
│   │   ├── js/
│   │   │   └── bundle.js       # Alpine.js + componentes
│   │   └── images/
│   └── custom/                 # Assets personalizados
│       ├── css/
│       └── js/
│           └── htmx.min.js
│
├── templates/                  # Templates Django
│   ├── base.html               # Template base
│   ├── base_auth.html          # Template autenticación
│   ├── dashboard.html          # Dashboard ejemplo
│   └── components/             # Componentes reutilizables
│       ├── header.html
│       ├── sidebar.html
│       ├── preloader.html
│       └── overlay.html
│
├── docs/                       # Documentación
│   ├── TAILWIND_INTEGRATION.md     # Integración Tailwind
│   ├── HTMX_GUIDE.md               # Guía HTMX
│   ├── FRONTEND_INTEGRATION.md     # Integración frontend
│   ├── PROJECT_STRUCTURE.md        # Estructura proyecto
│   └── tailadmin-html-pro-2.0-main/ # Fuente TailAdmin
│
├── manage.py
└── README.md
```

## 🎯 Características

### ✅ Implementado

- ✅ **Tailwind CSS v4** integrado y compilado
- ✅ **Alpine.js** para reactividad del cliente
- ✅ **HTMX** para interacciones AJAX
- ✅ **Dark Mode** con persistencia en localStorage
- ✅ **Responsive Design** (mobile, tablet, desktop)
- ✅ **Templates Base** listos para usar
- ✅ **Componentes Reutilizables** (header, sidebar, modals)
- ✅ **TailAdmin Pro** componentes premium integrados

### 🔜 Por Implementar

- Multi-tenant con django-tenants
- Sistema de autenticación
- Panel de administración SaaS
- Panel del cliente
- Gestión de usuarios y roles
- Catálogo de módulos
- Sistema de facturación

## 🚀 Instalación

### Requisitos Previos

- Python 3.11+
- Node.js (para compilar assets si es necesario)
- PostgreSQL (para producción)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/farreusadev/J250929D_SAAS.git
cd J250929D_SAAS
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias Python**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

7. **Acceder a la aplicación**
```
http://localhost:8000
```

## 📚 Documentación

### Guías Disponibles

- **[TAILWIND_INTEGRATION.md](docs/TAILWIND_INTEGRATION.md)** - Proceso completo de integración de Tailwind + TailAdmin
- **[HTMX_GUIDE.md](docs/HTMX_GUIDE.md)** - Guía completa de HTMX con ejemplos
- **[FRONTEND_INTEGRATION.md](docs/FRONTEND_INTEGRATION.md)** - Patrones de integración frontend
- **[PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - Estructura detallada del proyecto

### Inicio Rápido

#### Crear un nuevo template

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Mi Página{% endblock %}
{% block page_name %}mi-pagina{% endblock %}

{% block content %}
<div class="rounded-lg border border-gray-200 bg-white p-6">
    <h1 class="text-2xl font-semibold">¡Hola Mundo!</h1>
</div>
{% endblock %}
```

#### Usar HTMX para carga dinámica

```html
<button 
    hx-get="/api/data" 
    hx-target="#result"
    hx-swap="innerHTML"
    class="btn btn-primary"
>
    Cargar Datos
</button>

<div id="result">
    <!-- Los datos se cargarán aquí -->
</div>
```

#### Usar Alpine.js para interactividad

```html
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open">
        Contenido dinámico
    </div>
</div>
```

## 🎨 Componentes Disponibles

### Layouts
- `base.html` - Layout principal con sidebar y header
- `base_auth.html` - Layout para login/registro
- `dashboard.html` - Dashboard con stats cards

### Componentes
- `components/header.html` - Header con navbar y user dropdown
- `components/sidebar.html` - Sidebar responsive con menú
- `components/preloader.html` - Preloader animado
- `components/overlay.html` - Overlay para móvil

### Características
- **Dark Mode** - Toggle automático con persistencia
- **Responsive** - Mobile-first design
- **Sidebar Collapsible** - Desktop y mobile
- **User Dropdown** - Con avatar dinámico
- **Active Menu** - Basado en URL actual

## 🛠️ Desarrollo

### Compilar Assets de TailAdmin (si modificas)

```bash
cd docs/tailadmin-html-pro-2.0-main
npm install
npm run build
# Copiar archivos compilados a static/tailadmin/
```

### Ejecutar Tests

```bash
python manage.py test
```

### Crear Requirements

```bash
pip freeze > requirements.txt
```

## 📖 Mejores Prácticas

### Cuándo usar cada tecnología

- **Tailwind CSS**: Para TODOS los estilos
- **Alpine.js**: Para estado local y reactividad del cliente
- **HTMX**: Para comunicación con el servidor y AJAX
- **Django**: Para lógica de negocio y renderizado de templates

### Estructura de Templates

```
templates/
├── base.html                   # Layout principal
├── mi_app/
│   ├── list.html              # Vista completa
│   ├── _table.html            # Partial para HTMX
│   └── _form.html             # Partial para formularios
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Convenciones de Commits

- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Documentación
- `style:` - Formato (no afecta código)
- `refactor:` - Refactorización
- `test:` - Tests

## 📄 Licencia

Este proyecto es privado y propietario.

## 👥 Autor

- **Franklin Arredondo** - [farreusadev](https://github.com/farreusadev)

## 🔗 Enlaces

- **Repository**: https://github.com/farreusadev/J250929D_SAAS
- **TailAdmin Pro**: https://tailadmin.com
- **Tailwind CSS**: https://tailwindcss.com
- **Alpine.js**: https://alpinejs.dev
- **HTMX**: https://htmx.org

---

⭐ Si te gusta este proyecto, dale una estrella!
