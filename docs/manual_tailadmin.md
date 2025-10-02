# 📘 Manual Completo: TailAdmin Pro + Django

**Guía definitiva para integrar y usar TailAdmin Pro en proyectos Django**

Basado en el proyecto J250929D_SAAS

---

## 📑 Tabla de Contenidos

1. [Integración de TailAdmin en Django](#parte-1-integración-de-tailadmin-en-django)
2. [Uso e Implementación de Templates](#parte-2-uso-e-implementación-de-templates)
3. [Ejemplos Prácticos de Componentes](#parte-3-ejemplos-prácticos-de-componentes)

---

# PARTE 1: Integración de TailAdmin en Django

## 1.1 Requisitos Previos

### Software Necesario

```bash
# Verificar versiones instaladas
python --version    # Python 3.11+
node --version      # Node.js 18+
npm --version       # npm 9+
```

### Estructura Inicial del Proyecto

```
mi_proyecto/
├── config/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── docs/
    └── tailadmin-html-pro-2.0-main/  ← Carpeta descargada de TailAdmin Pro
```

---

## 1.2 Paso 1: Compilar Assets de TailAdmin

### 1.2.1 Instalar Dependencias

```bash
# Navegar a la carpeta de TailAdmin
cd docs/tailadmin-html-pro-2.0-main

# Instalar dependencias npm
npm install
```

**¿Qué instala?**
- Tailwind CSS v4.0
- Alpine.js v3.14
- Webpack (bundler)
- PostCSS (procesador CSS)
- ApexCharts, FullCalendar, Flatpickr, etc.

### 1.2.2 Compilar Assets

```bash
# Compilar assets para producción
npm run build
```

**Resultado:** Se crea la carpeta `build/` con:
```
build/
├── css/
│   ├── style.css      ← Tailwind compilado (~800KB)
│   └── prism.css      ← Syntax highlighting
├── js/
│   └── bundle.js      ← Alpine.js + componentes (~400KB)
└── images/            ← Imágenes optimizadas
```

### 1.2.3 Verificar Compilación

```bash
# Listar archivos compilados (Windows)
dir build

# Listar archivos compilados (Linux/Mac)
ls -lh build/
```

---

## 1.3 Paso 2: Configurar Estructura Django

### 1.3.1 Crear Carpetas Static y Templates

```bash
# Windows (PowerShell)
New-Item -Path "static/tailadmin/css" -ItemType Directory -Force
New-Item -Path "static/tailadmin/js" -ItemType Directory -Force
New-Item -Path "static/tailadmin/images" -ItemType Directory -Force
New-Item -Path "static/custom/css" -ItemType Directory -Force
New-Item -Path "static/custom/js" -ItemType Directory -Force
New-Item -Path "templates/components" -ItemType Directory -Force

# Linux/Mac
mkdir -p static/tailadmin/{css,js,images}
mkdir -p static/custom/{css,js}
mkdir -p templates/components
```

**Estructura resultante:**
```
proyecto/
├── static/
│   ├── tailadmin/          ← Assets de TailAdmin compilados
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── custom/             ← Assets personalizados del proyecto
│       ├── css/
│       └── js/
└── templates/
    └── components/         ← Componentes reutilizables
```

### 1.3.2 Copiar Assets Compilados

**Windows (PowerShell):**
```powershell
# Copiar CSS
Copy-Item "docs/tailadmin-html-pro-2.0-main/build/css/style.css" "static/tailadmin/css/"
Copy-Item "docs/tailadmin-html-pro-2.0-main/build/css/prism.css" "static/tailadmin/css/"

# Copiar JS
Copy-Item "docs/tailadmin-html-pro-2.0-main/build/js/bundle.js" "static/tailadmin/js/"

# Copiar imágenes
Copy-Item "docs/tailadmin-html-pro-2.0-main/src/images/*" "static/tailadmin/images/" -Recurse -Force

# Copiar favicon
Copy-Item "docs/tailadmin-html-pro-2.0-main/src/images/favicon.ico" "static/tailadmin/"
```

**Linux/Mac:**
```bash
# Copiar CSS
cp docs/tailadmin-html-pro-2.0-main/build/css/style.css static/tailadmin/css/
cp docs/tailadmin-html-pro-2.0-main/build/css/prism.css static/tailadmin/css/

# Copiar JS
cp docs/tailadmin-html-pro-2.0-main/build/js/bundle.js static/tailadmin/js/

# Copiar imágenes
cp -r docs/tailadmin-html-pro-2.0-main/src/images/* static/tailadmin/images/

# Copiar favicon
cp docs/tailadmin-html-pro-2.0-main/src/images/favicon.ico static/tailadmin/
```

### 1.3.3 Configurar Django Settings

**Editar `config/settings.py`:**

```python
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Carpeta donde collectstatic recopila archivos (para producción)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Carpetas adicionales de archivos estáticos (para desarrollo)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files (User uploads)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

**Explicación de cada configuración:**

- `STATIC_URL = "static/"`: URL pública para archivos estáticos. Django sirve archivos desde `/static/`
- `STATIC_ROOT`: Carpeta donde `python manage.py collectstatic` recopila todos los archivos para producción
- `STATICFILES_DIRS`: Lista de carpetas adicionales donde Django busca archivos estáticos en desarrollo
- `MEDIA_URL`: URL para archivos subidos por usuarios (avatars, documentos, etc.)
- `MEDIA_ROOT`: Carpeta física donde se guardan los archivos subidos

### 1.3.4 Actualizar .gitignore

**Agregar a `.gitignore`:**

```gitignore
# Node modules (para TailAdmin)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# TailAdmin build (mantener source, excluir build y node_modules)
docs/tailadmin-html-pro-2.0-main/build/
docs/tailadmin-html-pro-2.0-main/node_modules/

# Django static files (generados)
staticfiles/
/static/CACHE/

# Media files (subidos por usuarios - no commitear en git)
media/
```

---

## 1.4 Paso 3: Crear Template Base con TailAdmin

### 1.4.1 Template Base Principal

**Crear `templates/base.html`:**

```django
<!DOCTYPE html>
<html lang="es" 
      x-data="{ darkMode: localStorage.getItem('darkMode') === 'true' }" 
      x-init="$watch('darkMode', val => localStorage.setItem('darkMode', val))"
      :class="{ 'dark': darkMode }">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Proyecto{% endblock %} | J250929D SaaS</title>
    {% load static %}
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{% static 'tailadmin/favicon.ico' %}">
    
    <!-- TailAdmin CSS -->
    <link rel="stylesheet" href="{% static 'tailadmin/css/style.css' %}">
    
    <!-- CSS adicional por página -->
    {% block extra_css %}{% endblock %}
</head>
<body x-data="{ sidebarOpen: false }" 
      x-bind:class="sidebarOpen ? 'overflow-hidden lg:overflow-visible' : ''" 
      class="bg-gray-100 dark:bg-gray-900"
      data-page-name="{% block page_name %}{% endblock %}">
    
    <!-- Preloader -->
    {% include 'components/preloader.html' %}
    
    <!-- Page Wrapper -->
    <div class="flex h-screen overflow-hidden">
        
        <!-- Sidebar -->
        {% include 'components/sidebar.html' %}
        
        <!-- Overlay para móvil -->
        {% include 'components/overlay.html' %}
        
        <!-- Content Area -->
        <div class="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
            
            <!-- Header -->
            {% include 'components/header.html' %}
            
            <!-- Main Content -->
            <main class="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
                
                <!-- Django Messages -->
                {% if messages %}
                <div class="mb-6 space-y-4">
                    {% for message in messages %}
                    {% include 'components/alert.html' with type=message.tags message=message %}
                    {% endfor %}
                </div>
                {% endif %}
                
                <!-- Page Content -->
                {% block content %}{% endblock %}
                
            </main>
            
        </div>
        
    </div>
    
    <!-- TailAdmin JS Bundle (Alpine.js + Componentes) -->
    <script src="{% static 'tailadmin/js/bundle.js' %}"></script>
    
    <!-- JS adicional por página -->
    {% block extra_js %}{% endblock %}
    
</body>
</html>
```

**Explicación línea por línea de Alpine.js:**

```html
<!-- Alpine.js data para dark mode -->
x-data="{ darkMode: localStorage.getItem('darkMode') === 'true' }"
<!-- Crea variable reactiva 'darkMode', lee valor desde localStorage -->

x-init="$watch('darkMode', val => localStorage.setItem('darkMode', val))"
<!-- Inicializa watcher: cuando darkMode cambia, guarda en localStorage -->

:class="{ 'dark': darkMode }"
<!-- Binding de clase: aplica 'dark' cuando darkMode es true -->

{% load static %}
<!-- Carga el template tag 'static' de Django para usar {% static '...' %} -->

{% block title %}{% endblock %}
<!-- Bloque reemplazable en templates hijos -->

x-data="{ sidebarOpen: false }"
<!-- Estado del sidebar (abierto/cerrado) para mobile -->
```

### 1.4.2 Crear Componentes Base

#### **Preloader Component**

**`templates/components/preloader.html`:**

```django
<!-- Preloader - Se oculta automáticamente al cargar la página -->
<div x-show="loaded" 
     x-init="window.addEventListener('DOMContentLoaded', () => { setTimeout(() => loaded = false, 500) })"
     x-data="{ loaded: true }"
     class="fixed left-0 top-0 z-999999 flex h-screen w-screen items-center justify-center bg-white dark:bg-black"
     style="display: none;">
    <div class="h-16 w-16 animate-spin rounded-full border-4 border-solid border-primary border-t-transparent"></div>
</div>
```

#### **Overlay Component**

**`templates/components/overlay.html`:**

```django
<!-- Overlay para móvil - Aparece cuando sidebar está abierto -->
<div x-show="sidebarOpen"
     @click="sidebarOpen = false"
     x-transition.opacity
     class="fixed inset-0 z-9998 bg-black/20 dark:bg-black/40 lg:hidden"></div>
```

#### **Alert Component**

**`templates/components/alert.html`:**

```django
<!-- Alert Component Reutilizable -->
<div class="flex w-full border-l-6 
     {% if type == 'success' %}border-success-500 bg-success-50 dark:bg-success-900/20
     {% elif type == 'error' %}border-error-500 bg-error-50 dark:bg-error-900/20
     {% elif type == 'warning' %}border-warning-500 bg-warning-50 dark:bg-warning-900/20
     {% else %}border-primary bg-primary/10{% endif %} 
     px-7 py-8 shadow-md md:p-9">
    <div class="mr-5 flex h-9 w-9 items-center justify-center rounded-lg 
         {% if type == 'success' %}bg-success-500
         {% elif type == 'error' %}bg-error-500
         {% elif type == 'warning' %}bg-warning-500
         {% else %}bg-primary{% endif %}">
        <!-- Icon SVG -->
        {% if type == 'success' %}
        <svg width="16" height="12" viewBox="0 0 16 12" fill="none">
            <path d="M15.2984 0.826822L15.2868 0.811827L15.2741 0.797751C14.9173 0.401867 14.3238 0.400754 13.9657 0.794406L5.91888 9.45376L2.05667 5.2868C1.69856 4.89287 1.10487 4.89389 0.747996 5.28987C0.417335 5.65675 0.417335 6.22337 0.747996 6.59026L0.747959 6.59029L0.752701 6.59541L4.86742 11.0348C5.14445 11.3405 5.52858 11.5 5.89581 11.5C6.29242 11.5 6.65178 11.3355 6.92401 11.035L15.2162 2.11161C15.5833 1.74452 15.576 1.18615 15.2984 0.826822Z" fill="white" stroke="white"/>
        </svg>
        {% elif type == 'error' %}
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 0C3.58172 0 0 3.58172 0 8C0 12.4183 3.58172 16 8 16C12.4183 16 16 12.4183 16 8C16 3.58172 12.4183 0 8 0ZM11.5 10.0859L10.0859 11.5L8 9.41406L5.91406 11.5L4.5 10.0859L6.58594 8L4.5 5.91406L5.91406 4.5L8 6.58594L10.0859 4.5L11.5 5.91406L9.41406 8L11.5 10.0859Z" fill="white"/>
        </svg>
        {% endif %}
    </div>
    <div class="w-full">
        <p class="text-base leading-relaxed 
           {% if type == 'success' %}text-success-800 dark:text-success-300
           {% elif type == 'error' %}text-error-800 dark:text-error-300
           {% elif type == 'warning' %}text-warning-800 dark:text-warning-300
           {% else %}text-gray-800 dark:text-gray-300{% endif %}">
            {{ message }}
        </p>
    </div>
</div>
```

---

## 1.5 Paso 4: Verificar Instalación

### 1.5.1 Verificar Django

```bash
# Verificar que no hay errores de configuración
python manage.py check

# Salida esperada:
# System check identified no issues (0 silenced).
```

### 1.5.2 Crear Vista de Prueba

**En tu app, crear `views.py`:**

```python
from django.shortcuts import render

def test_tailadmin(request):
    """Vista de prueba para verificar TailAdmin"""
    return render(request, 'test_tailadmin.html')
```

**Agregar URL en `urls.py`:**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_tailadmin, name='test_tailadmin'),
]
```

**Crear `templates/test_tailadmin.html`:**

```django
{% extends 'base.html' %}

{% block title %}Test TailAdmin{% endblock %}

{% block content %}
<div class="rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
        ✅ TailAdmin Funciona Correctamente!
    </h1>
    <p class="mt-4 text-gray-600 dark:text-gray-300">
        Si ves este mensaje con estilos de Tailwind, la integración fue exitosa.
    </p>
    
    <!-- Test Dark Mode Toggle -->
    <div class="mt-6" x-data="{ show: true }">
        <button @click="darkMode = !darkMode" 
                class="rounded-lg bg-primary px-6 py-3 font-medium text-white hover:bg-opacity-90">
            🌙 Toggle Dark Mode
        </button>
        
        <button @click="show = !show"
                class="ml-4 rounded-lg bg-secondary px-6 py-3 font-medium text-white hover:bg-opacity-90">
            ⚡ Toggle Text (Alpine.js Test)
        </button>
        
        <p x-show="show" class="mt-4 text-lg">
            Alpine.js está funcionando! 🎉
        </p>
    </div>
</div>
{% endblock %}
```

### 1.5.3 Probar en Navegador

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Abrir en navegador
http://localhost:8000/test/
```

**Verificar que funciona:**
- ✅ Los estilos de Tailwind se aplican correctamente
- ✅ El botón de dark mode cambia el tema
- ✅ El botón de Alpine.js muestra/oculta texto
- ✅ No hay errores 404 en la consola del navegador
- ✅ Los colores de TailAdmin (primary, secondary) son visibles

---

## 1.6 Troubleshooting Común

### ❌ Problema 1: "Archivo CSS no encontrado (404)"

**Síntoma:** En la consola del navegador aparece error 404 para `style.css`

**Solución:**
```bash
# 1. Verificar que el archivo existe
ls static/tailadmin/css/style.css

# 2. Si no existe, copiar de nuevo desde build
cp docs/tailadmin-html-pro-2.0-main/build/css/style.css static/tailadmin/css/

# 3. Verificar settings.py
# Debe tener: STATICFILES_DIRS = [BASE_DIR / "static"]
```

### ❌ Problema 2: "Estilos no se aplican"

**Verificar en este orden:**

1. **Settings configurado correctamente:**
```python
# config/settings.py
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

2. **Template tag cargado:**
```django
{% load static %}  ← Debe estar al inicio del template
```

3. **Ruta correcta en template:**
```django
<!-- ✅ Correcto -->
<link rel="stylesheet" href="{% static 'tailadmin/css/style.css' %}">

<!-- ❌ Incorrecto -->
<link rel="stylesheet" href="/static/tailadmin/css/style.css">
```

4. **Servidor reiniciado:**
```bash
# Detener servidor (Ctrl+C) y reiniciar
python manage.py runserver
```

### ❌ Problema 3: "Alpine.js no funciona (dark mode no cambia)"

**Verificar:**

1. **bundle.js se carga:**
```django
<script src="{% static 'tailadmin/js/bundle.js' %}"></script>
```

2. **bundle.js existe:**
```bash
ls static/tailadmin/js/bundle.js
```

3. **Sintaxis Alpine.js correcta:**
```html
<!-- ✅ Correcto -->
<div x-data="{ open: false }">

<!-- ❌ Incorrecto (falta {}) -->
<div x-data="open: false">
```

4. **Inspeccionar en DevTools:**
- Abrir DevTools (F12)
- Ir a Console
- Escribir: `Alpine`
- Debe mostrar objeto Alpine.js, no "undefined"

### ❌ Problema 4: "Dark mode no persiste al recargar"

**Causa:** localStorage no funciona

**Verificar:**
```html
<!-- En <html> tag debe estar: -->
x-data="{ darkMode: localStorage.getItem('darkMode') === 'true' }"
x-init="$watch('darkMode', val => localStorage.setItem('darkMode', val))"
```

**Debug en Console:**
```javascript
// Verificar que se guarda
localStorage.getItem('darkMode')  // Debe devolver 'true' o 'false'
```

---

# PARTE 2: Uso e Implementación de Templates

## 2.1 Sistema de Herencia de Templates Django

### 2.1.1 Jerarquía de Templates

```
┌─────────────────────────────────────┐
│         base.html                   │  ← Template maestro
│  (header, sidebar, estructura)      │
└──────────┬──────────────────────────┘
           │
     ┌─────┴─────┐
     │           │
┌────▼────┐  ┌──▼──────────┐
│base_auth│  │dashboard.html│  ← Templates intermedios
└────┬────┘  └──┬───────────┘
     │          │
┌────▼────┐ ┌──▼──────────┐
│login.html│ │users/list.html│  ← Templates finales
└─────────┘ └──────────────┘
```

### 2.1.2 Bloques Disponibles en base.html

```django
{% block title %}          <!-- Título de la página (<title>) -->
{% block page_name %}      <!-- Identificador de página (data-page-name) -->
{% block extra_css %}      <!-- CSS adicional antes de </head> -->
{% block content %}        <!-- Contenido principal de la página -->
{% block extra_js %}       <!-- JS adicional antes de </body> -->
```

---

## 2.2 Crear Templates Hijos

### 2.2.1 Template Simple

**`templates/mi_app/dashboard.html`:**

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard{% endblock %}
{% block page_name %}dashboard{% endblock %}

{% block content %}
<div class="rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        Dashboard
    </h1>
    <p class="mt-4 text-gray-600 dark:text-gray-300">
        Bienvenido al panel de administración
    </p>
</div>
{% endblock %}
```

**Explicación:**

```django
{% extends 'base.html' %}
<!-- Hereda de base.html: incluye header, sidebar, footer, etc. -->

{% load static %}
<!-- Carga template tag para usar {% static '...' %} -->

{% block title %}Dashboard{% endblock %}
<!-- Reemplaza el bloque 'title' de base.html -->
<!-- Resultado: <title>Dashboard | J250929D SaaS</title> -->

{% block content %}
    <!-- Tu contenido aquí -->
{% endblock %}
<!-- Reemplaza el bloque 'content' de base.html -->
<!-- Este contenido aparecerá en el área principal -->
```

### 2.2.2 Template con CSS y JS Adicional

**`templates/mi_app/dashboard_advanced.html`:**

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard Avanzado{% endblock %}

{% block extra_css %}
<!-- CSS específico para esta página -->
<link rel="stylesheet" href="{% static 'custom/css/dashboard.css' %}">
<style>
    .custom-chart {
        height: 400px;
    }
</style>
{% endblock %}

{% block content %}
<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
    <!-- Stats Cards -->
    <div class="rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Total Users</p>
                <h3 class="mt-1 text-3xl font-bold text-gray-900 dark:text-white">
                    {{ total_users|default:'1,234' }}
                </h3>
            </div>
            <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                <svg class="h-6 w-6 text-primary" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                </svg>
            </div>
        </div>
    </div>
    <!-- Más stats cards... -->
</div>

<!-- Chart Container -->
<div class="mt-6 rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Estadísticas Mensuales
    </h3>
    <div id="chart-container" class="custom-chart"></div>
</div>
{% endblock %}

{% block extra_js %}
<!-- JS específico para esta página -->
<script src="{% static 'custom/js/dashboard.js' %}"></script>
<script>
    // Código inline específico
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Dashboard cargado');
        // Inicializar gráficos, etc.
    });
</script>
{% endblock %}
```

---

## 2.3 Componentes Reutilizables con `{% include %}`

### 2.3.1 ¿Qué son los Componentes?

Los componentes son templates pequeños y reutilizables que se incluyen en otros templates.

**Ventajas:**
- ✅ **DRY (Don't Repeat Yourself):** Código reutilizable
- ✅ **Mantenibilidad:** Cambios en un solo lugar
- ✅ **Modularidad:** Componentes independientes
- ✅ **Testing:** Más fácil de probar

### 2.3.2 Crear un Componente Simple

#### **Ejemplo: User Card Component**

**`templates/components/user_card.html`:**

```django
<!-- User Card Component -->
<div class="rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
    <div class="flex items-center gap-4">
        <!-- Avatar -->
        {% if user.avatar %}
            <img src="{{ user.avatar.url }}" 
                 alt="{{ user.get_full_name }}" 
                 class="h-16 w-16 rounded-full object-cover">
        {% else %}
            <img src="{% static 'tailadmin/images/user/owner.png' %}" 
                 alt="{{ user.get_full_name }}" 
                 class="h-16 w-16 rounded-full">
        {% endif %}
        
        <!-- Info -->
        <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ user.get_full_name|default:user.username }}
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ user.email }}
            </p>
            <span class="mt-2 inline-block rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
                {{ user.role|default:'User' }}
            </span>
        </div>
    </div>
    
    <!-- Actions -->
    <div class="mt-4 flex gap-2">
        <a href="{% url 'users:edit' user.id %}" 
           class="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-opacity-90">
            Editar
        </a>
        <a href="{% url 'users:view' user.id %}" 
           class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700">
            Ver Detalles
        </a>
    </div>
</div>
```

#### **Usar el Componente:**

```django
{% extends 'base.html' %}

{% block content %}
<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
    {% for user in users %}
        {% include 'components/user_card.html' with user=user %}
    {% endfor %}
</div>
{% endblock %}
```

### 2.3.3 Componente con Parámetros

#### **Ejemplo: Stat Card Component**

**`templates/components/stat_card.html`:**

```django
<!-- Stat Card Component -->
<div class="rounded-lg border border-gray-200 bg-white px-7.5 py-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
    <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-{{ color|default:'primary' }}/10">
        {{ icon|safe }}
    </div>
    
    <div class="mt-4 flex items-end justify-between">
        <div>
            <h4 class="text-title-md font-bold text-gray-900 dark:text-white">
                {{ value }}
            </h4>
            <span class="text-sm font-medium text-gray-500 dark:text-gray-400">
                {{ label }}
            </span>
        </div>
        
        {% if percentage %}
        <span class="flex items-center gap-1 text-sm font-medium 
              {% if percentage > 0 %}text-success-500{% else %}text-error-500{% endif %}">
            {{ percentage }}%
            <svg class="fill-current {% if percentage < 0 %}rotate-180{% endif %}" 
                 width="10" height="11" viewBox="0 0 10 11">
                <path d="M4.35716 2.47737L0.908974 5.82987L5.0443e-07 4.94612L5 0.0848689L10 4.94612L9.09103 5.82987L5.64284 2.47737L5.64284 10.0849L4.35716 10.0849L4.35716 2.47737Z"/>
            </svg>
        </span>
        {% endif %}
    </div>
</div>
```

#### **Usar con parámetros:**

```django
{% extends 'base.html' %}

{% block content %}
<div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
    
    <!-- Card 1 -->
    {% include 'components/stat_card.html' with 
        value='$3.456K' 
        label='Total views' 
        color='primary' 
        percentage=0.43
        icon='<svg class="fill-primary" width="22" height="16"><path d="..."/></svg>'
    %}
    
    <!-- Card 2 -->
    {% include 'components/stat_card.html' with 
        value='$45,2K' 
        label='Total Profit' 
        color='success' 
        percentage=4.35
        icon='<svg>...</svg>'
    %}
    
    <!-- Card 3 -->
    {% include 'components/stat_card.html' with 
        value='2.450' 
        label='Total Products' 
        color='warning' 
        percentage=-2.15
        icon='<svg>...</svg>'
    %}
    
    <!-- Card 4 -->
    {% include 'components/stat_card.html' with 
        value='3.456' 
        label='Total Users' 
        color='secondary' 
        percentage=0.95
        icon='<svg>...</svg>'
    %}
    
</div>
{% endblock %}
```

---

## 2.4 Convertir HTML de TailAdmin a Django Template

### 2.4.1 Proceso Paso a Paso

**HTML Original de TailAdmin (`src/index.html`):**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="rounded-lg bg-white p-6 shadow-md">
        <h2 class="text-xl font-semibold">Dashboard</h2>
        <p>Welcome to your dashboard</p>
    </div>
    <script src="js/bundle.js"></script>
</body>
</html>
```

**Paso 1: Identificar estructura**
- Header (`<head>`)
- Body content
- Scripts

**Paso 2: Convertir a Django**

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard{% endblock %}
{% block page_name %}dashboard{% endblock %}

{% block content %}
<!-- Contenido del body original -->
<div class="rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
    <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
        Dashboard
    </h2>
    <p class="text-gray-600 dark:text-gray-300">
        Welcome to your dashboard
    </p>
</div>
{% endblock %}
```

**Cambios realizados:**
1. ✅ Agregado `{% extends 'base.html' %}` (hereda estructura)
2. ✅ Agregado `{% load static %}` (para archivos estáticos)
3. ✅ Wrapped content en `{% block content %}`
4. ✅ Agregado dark mode classes (`dark:bg-gray-800`, `dark:text-white`)
5. ✅ Agregado classes de color de texto (`text-gray-900`, `text-gray-600`)
6. ✅ Eliminado `<html>`, `<head>`, `<body>` (viene de base.html)

### 2.4.2 Convertir Partial de TailAdmin

**TailAdmin Partial (`src/partials/cards/card-01.html`):**

```html
<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
    <div class="flex items-center">
        <div class="flex h-11 w-11 items-center justify-center rounded-full bg-primary/10">
            <svg class="h-5 w-5 text-primary" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/>
            </svg>
        </div>
        <div class="ml-4">
            <h4 class="text-2xl font-bold text-gray-900">3.456</h4>
            <span class="text-sm text-gray-500">Total Users</span>
        </div>
    </div>
</div>
```

**Convertir a Componente Django Parametrizable:**

**`templates/components/cards/stat_simple.html`:**

```django
<!-- Stat Card Simple Component -->
<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
    <div class="flex items-center">
        <div class="flex h-11 w-11 items-center justify-center rounded-full bg-{{ color|default:'primary' }}/10">
            {{ icon|safe }}
        </div>
        <div class="ml-4">
            <h4 class="text-2xl font-bold text-gray-900 dark:text-white">
                {{ value }}
            </h4>
            <span class="text-sm text-gray-500 dark:text-gray-400">
                {{ label }}
            </span>
        </div>
    </div>
</div>
```

**Usar el componente:**

```django
{% extends 'base.html' %}

{% block content %}
<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
    
    {% include 'components/cards/stat_simple.html' with 
        value=total_users 
        label='Total Users' 
        color='primary' 
        icon='<svg class="h-5 w-5 text-primary" fill="currentColor" viewBox="0 0 20 20"><path d="..."/></svg>'
    %}
    
    {% include 'components/cards/stat_simple.html' with 
        value=total_products 
        label='Total Products' 
        color='success' 
        icon='<svg>...</svg>'
    %}
    
</div>
{% endblock %}
```

---

## 2.5 Trabajar con Imágenes y Assets

### 2.5.1 Usar Imágenes de TailAdmin

```django
<!-- Logo (cambia según dark mode) -->
<img src="{% static 'tailadmin/images/logo/logo.svg' %}" 
     alt="Logo" 
     class="h-10 w-10 dark:hidden">
<img src="{% static 'tailadmin/images/logo/logo-dark.svg' %}" 
     alt="Logo" 
     class="hidden h-10 w-10 dark:block">

<!-- User Avatar predeterminado -->
<img src="{% static 'tailadmin/images/user/user-01.jpg' %}" 
     alt="User" 
     class="h-10 w-10 rounded-full object-cover">

<!-- Iconos -->
<img src="{% static 'tailadmin/images/icons/file-pdf.svg' %}" 
     alt="PDF" 
     class="h-6 w-6">

<!-- Brand logos -->
<img src="{% static 'tailadmin/images/brand/brand-01.svg' %}" 
     alt="Google" 
     class="h-8">
```

### 2.5.2 Usar Imágenes Subidas por Usuarios

```django
<!-- Avatar del usuario con fallback -->
{% if user.avatar %}
    <img src="{{ user.avatar.url }}" 
         alt="{{ user.get_full_name }}" 
         class="h-10 w-10 rounded-full object-cover">
{% else %}
    <img src="{% static 'tailadmin/images/user/owner.png' %}" 
         alt="{{ user.get_full_name }}" 
         class="h-10 w-10 rounded-full">
{% endif %}

<!-- Imagen de producto con placeholder -->
{% if product.image %}
    <img src="{{ product.image.url }}" 
         alt="{{ product.name }}" 
         class="h-48 w-full object-cover">
{% else %}
    <div class="flex h-48 w-full items-center justify-center bg-gray-100 dark:bg-gray-700">
        <svg class="h-12 w-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z"/>
        </svg>
    </div>
{% endif %}
```

### 2.5.3 Lazy Loading de Imágenes

```django
<!-- Lazy loading nativo del navegador -->
<img src="{% static 'tailadmin/images/large-image.jpg' %}" 
     alt="Description" 
     loading="lazy"
     class="h-64 w-full object-cover">

<!-- Con Alpine.js (para más control) -->
<img x-data="{ loaded: false }"
     x-bind:src="loaded ? '{{ product.image.url }}' : '{% static 'tailadmin/images/placeholder.svg' %}'"
     x-intersect="loaded = true"
     alt="{{ product.name }}"
     class="h-48 w-full object-cover">
```

---

# PARTE 3: Ejemplos Prácticos de Componentes

## 3.1 Ejemplo Completo: Lista de Usuarios (CRUD)

### 3.1.1 Vista (View)

**`apps/users/views.py`:**

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm

@login_required
def user_list(request):
    """Lista de usuarios con búsqueda y paginación"""
    # Obtener parámetro de búsqueda
    search_query = request.GET.get('q', '')
    
    # Filtrar usuarios
    users = User.objects.all()
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Ordenar
    users = users.order_by('-date_joined')
    
    # Paginar
    paginator = Paginator(users, 10)  # 10 usuarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search_query': search_query,
        'total_users': User.objects.count(),
    }
    return render(request, 'users/list.html', context)
```

### 3.1.2 Template

**`templates/users/list.html`:**

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Usuarios{% endblock %}
{% block page_name %}users-list{% endblock %}

{% block content %}
<!-- Breadcrumb -->
<div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
    <h2 class="text-title-md2 font-bold text-gray-900 dark:text-white">
        Usuarios
    </h2>
    
    <nav>
        <ol class="flex items-center gap-2">
            <li>
                <a href="{% url 'dashboard' %}" 
                   class="font-medium text-gray-500 hover:text-primary dark:text-gray-400">
                    Dashboard /
                </a>
            </li>
            <li class="font-medium text-primary">Usuarios</li>
        </ol>
    </nav>
</div>

<!-- Stats Overview -->
<div class="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">
    {% include 'components/stat_card.html' with 
        value=total_users 
        label='Total Usuarios' 
        color='primary'
        icon='<svg class="h-6 w-6 text-primary">...</svg>'
    %}
    <!-- Más stats... -->
</div>

<!-- Filters and Actions -->
<div class="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
    <!-- Search Bar -->
    <div class="relative w-full max-w-sm">
        <form method="get" action="">
            <input type="text" 
                   name="q"
                   value="{{ search_query }}"
                   placeholder="Buscar usuarios..."
                   class="w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-gray-900 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-800 dark:text-white">
            <span class="absolute left-3 top-1/2 -translate-y-1/2">
                <svg class="fill-gray-500" width="20" height="20" viewBox="0 0 20 20">
                    <path d="M19.7555 18.6065L16.3182 15.2458C17.5555 13.6065 18.2 11.6315 18.2 9.5C18.2 4.26152 13.9387 0 8.7 0C3.46127 0 -0.799988 4.26152 -0.799988 9.5C-0.799988 14.7385 3.46127 19 8.7 19C10.7555 19 12.6737 18.3815 14.3 17.2458L17.7373 20.6065C18.0555 20.9246 18.4782 21.0837 18.9009 21.0837C19.3237 21.0837 19.7464 20.9246 20.0645 20.6065C20.7009 19.97 20.7009 18.9429 19.7555 18.6065ZM8.7 16C5.26127 16 2.5 13.2387 2.5 9.8C2.5 6.36127 5.26127 3.6 8.7 3.6C12.1387 3.6 14.9 6.36127 14.9 9.8C14.9 13.2387 12.1387 16 8.7 16Z"/>
                </svg>
            </span>
        </form>
    </div>
    
    <!-- Add Button -->
    <a href="{% url 'users:create' %}" 
       class="inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-6 py-3 font-medium text-white hover:bg-opacity-90">
        <svg class="fill-current" width="20" height="20" viewBox="0 0 20 20">
            <path d="M10 0C4.47715 0 0 4.47715 0 10C0 15.5228 4.47715 20 10 20C15.5228 20 20 15.5228 20 10C20 4.47715 15.5228 0 10 0ZM15 11H11V15H9V11H5V9H9V5H11V9H15V11Z"/>
        </svg>
        Nuevo Usuario
    </a>
</div>

<!-- Users Table -->
<div class="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800">
    <div class="overflow-x-auto">
        <table class="w-full table-auto">
            <thead>
                <tr class="border-b border-gray-200 bg-gray-50 text-left dark:border-gray-700 dark:bg-gray-900">
                    <th class="min-w-[220px] px-4 py-4 font-medium text-gray-900 dark:text-white xl:pl-11">
                        Usuario
                    </th>
                    <th class="min-w-[150px] px-4 py-4 font-medium text-gray-900 dark:text-white">
                        Email
                    </th>
                    <th class="min-w-[120px] px-4 py-4 font-medium text-gray-900 dark:text-white">
                        Rol
                    </th>
                    <th class="min-w-[120px] px-4 py-4 font-medium text-gray-900 dark:text-white">
                        Estado
                    </th>
                    <th class="px-4 py-4 font-medium text-gray-900 dark:text-white">
                        Acciones
                    </th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr class="border-b border-gray-200 dark:border-gray-700">
                    <!-- Usuario -->
                    <td class="px-4 py-5 pl-9 xl:pl-11">
                        <div class="flex items-center gap-3">
                            {% if user.avatar %}
                                <img src="{{ user.avatar.url }}" 
                                     alt="{{ user.get_full_name }}" 
                                     class="h-10 w-10 rounded-full object-cover">
                            {% else %}
                                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                                    <span class="font-medium text-primary">
                                        {{ user.get_full_name|first|upper }}
                                    </span>
                                </div>
                            {% endif %}
                            <div class="flex flex-col">
                                <span class="font-medium text-gray-900 dark:text-white">
                                    {{ user.get_full_name|default:user.username }}
                                </span>
                                <span class="text-sm text-gray-500 dark:text-gray-400">
                                    @{{ user.username }}
                                </span>
                            </div>
                        </div>
                    </td>
                    
                    <!-- Email -->
                    <td class="px-4 py-5">
                        <span class="text-gray-600 dark:text-gray-300">
                            {{ user.email }}
                        </span>
                    </td>
                    
                    <!-- Rol -->
                    <td class="px-4 py-5">
                        <span class="inline-flex rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
                            {{ user.get_role_display|default:'User' }}
                        </span>
                    </td>
                    
                    <!-- Estado -->
                    <td class="px-4 py-5">
                        {% if user.is_active %}
                        <span class="inline-flex rounded-full bg-success-500/10 px-3 py-1 text-sm font-medium text-success-500">
                            <span class="mr-1">●</span> Activo
                        </span>
                        {% else %}
                        <span class="inline-flex rounded-full bg-error-500/10 px-3 py-1 text-sm font-medium text-error-500">
                            <span class="mr-1">●</span> Inactivo
                        </span>
                        {% endif %}
                    </td>
                    
                    <!-- Acciones -->
                    <td class="px-4 py-5">
                        <div class="flex items-center space-x-3.5">
                            <!-- Ver -->
                            <a href="{% url 'users:detail' user.id %}" 
                               class="hover:text-primary"
                               title="Ver detalles">
                                <svg class="fill-current" width="18" height="18" viewBox="0 0 18 18">
                                    <path d="M8.99981 14.8219C3.43106 14.8219 0.674805 9.50624 0.562305 9.28124C0.47793 9.11249 0.47793 8.88749 0.562305 8.71874C0.674805 8.49374 3.43106 3.20624 8.99981 3.20624C14.5686 3.20624 17.3248 8.49374 17.4373 8.71874C17.5217 8.88749 17.5217 9.11249 17.4373 9.28124C17.3248 9.50624 14.5686 14.8219 8.99981 14.8219ZM1.85605 8.99999C2.4748 10.0406 4.89356 13.5562 8.99981 13.5562C13.1061 13.5562 15.5248 10.0406 16.1436 8.99999C15.5248 7.95936 13.1061 4.44374 8.99981 4.44374C4.89356 4.44374 2.4748 7.95936 1.85605 8.99999Z"/>
                                    <path d="M9 11.3906C7.67812 11.3906 6.60938 10.3219 6.60938 9C6.60938 7.67813 7.67812 6.60938 9 6.60938C10.3219 6.60938 11.3906 7.67813 11.3906 9C11.3906 10.3219 10.3219 11.3906 9 11.3906ZM9 7.875C8.38125 7.875 7.875 8.38125 7.875 9C7.875 9.61875 8.38125 10.125 9 10.125C9.61875 10.125 10.125 9.61875 10.125 9C10.125 8.38125 9.61875 7.875 9 7.875Z"/>
                                </svg>
                            </a>
                            
                            <!-- Editar -->
                            <a href="{% url 'users:edit' user.id %}" 
                               class="hover:text-primary"
                               title="Editar">
                                <svg class="fill-current" width="18" height="18" viewBox="0 0 18 18">
                                    <path d="M16.0547 1.94609C15.0937 0.985092 13.5234 0.985092 12.5625 1.94609L5.11719 9.39141C4.95469 9.55391 4.84922 9.77109 4.79297 9.98828L3.78516 13.5352C3.67969 13.918 3.78516 14.3289 4.06641 14.6102C4.29297 14.8367 4.60469 14.9422 4.91641 14.9422C5.02188 14.9422 5.12734 14.9422 5.23281 14.9141L8.77969 13.9063C8.99688 13.85 9.21406 13.7445 9.37656 13.582L16.8219 6.13672C17.3789 5.55234 17.6602 4.79609 17.6602 4.01172C17.6602 3.22734 17.3508 2.50312 16.0547 1.94609ZM8.00234 12.4109L5.78516 13.082L6.45625 10.8648L11.9484 5.37266L12.6195 6.04375L8.00234 12.4109ZM15.4688 4.84453L14.3437 5.96953L13.6727 5.29844L14.7977 4.17344C15.1367 3.83437 15.6656 3.83437 16.0047 4.17344C16.1672 4.33594 16.2727 4.55312 16.2727 4.77031C16.2727 4.98750 16.1672 5.20469 15.4688 4.84453Z"/>
                                    <path d="M14.625 12.0938V14.625C14.625 15.5859 13.8633 16.3477 12.9023 16.3477H3.375C2.41406 16.3477 1.65234 15.5859 1.65234 14.625V5.09766C1.65234 4.13672 2.41406 3.375 3.375 3.375H8.04297C8.36719 3.375 8.66484 3.12891 8.66484 2.77734C8.66484 2.42578 8.41875 2.15234 8.04297 2.15234H3.375C1.70859 2.15234 0.3125 3.54844 0.3125 5.21484V14.7422C0.3125 16.4086 1.70859 17.8047 3.375 17.8047H12.9023C14.5687 17.8047 15.9648 16.4086 15.9648 14.7422V12.0937C15.9648 11.7695 15.7187 11.4719 15.3672 11.4719C15.0156 11.4719 14.625 11.7422 14.625 12.0938Z"/>
                                </svg>
                            </a>
                            
                            <!-- Eliminar -->
                            <form method="post" action="{% url 'users:delete' user.id %}" 
                                  onsubmit="return confirm('¿Estás seguro de eliminar este usuario?');"
                                  class="inline">
                                {% csrf_token %}
                                <button type="submit" 
                                        class="hover:text-error-500"
                                        title="Eliminar">
                                    <svg class="fill-current" width="18" height="18" viewBox="0 0 18 18">
                                        <path d="M13.7535 2.47502H11.5879V1.9969C11.5879 1.15315 10.9129 0.478149 10.0691 0.478149H7.90352C7.05977 0.478149 6.38477 1.15315 6.38477 1.9969V2.47502H4.21914C3.40352 2.47502 2.72852 3.15002 2.72852 3.96565V4.8094C2.72852 5.42815 3.09414 5.9344 3.62852 6.1594L4.07852 15.4688C4.13477 16.6219 5.09102 17.5219 6.24414 17.5219H11.7004C12.8535 17.5219 13.8098 16.6219 13.866 15.4688L14.3441 6.13127C14.8785 5.90627 15.2441 5.3719 15.2441 4.78127V3.93752C15.2441 3.15002 14.5691 2.47502 13.7535 2.47502ZM7.67852 1.9969C7.67852 1.85627 7.79102 1.74377 7.93164 1.74377H10.0973C10.2379 1.74377 10.3504 1.85627 10.3504 1.9969V2.47502H7.70664V1.9969H7.67852ZM4.02227 3.96565C4.02227 3.85315 4.10664 3.74065 4.24727 3.74065H13.7535C13.866 3.74065 13.9785 3.82502 13.9785 3.96565V4.8094C13.9785 4.9219 13.8941 5.0344 13.7535 5.0344H4.24727C4.13477 5.0344 4.02227 4.95002 4.02227 4.8094V3.96565ZM11.7285 16.2563H6.27227C5.79414 16.2563 5.40039 15.8906 5.37227 15.3844L4.95039 6.2719H13.0785L12.6566 15.3844C12.6004 15.8625 12.2066 16.2563 11.7285 16.2563Z"/>
                                        <path d="M9.00039 9.11255C8.66289 9.11255 8.35352 9.3938 8.35352 9.75942V13.3313C8.35352 13.6688 8.63477 13.9782 9.00039 13.9782C9.33789 13.9782 9.64727 13.6969 9.64727 13.3313V9.75942C9.64727 9.3938 9.33789 9.11255 9.00039 9.11255Z"/>
                                        <path d="M11.2502 9.67504C10.8846 9.64692 10.6033 9.90004 10.5752 10.2657L10.4064 12.7407C10.3783 13.0782 10.6314 13.3875 10.9971 13.4157C11.0252 13.4157 11.0252 13.4157 11.0533 13.4157C11.3908 13.4157 11.6721 13.1625 11.6721 12.825L11.8408 10.35C11.8408 9.98442 11.5877 9.70317 11.2502 9.67504Z"/>
                                        <path d="M6.72245 9.67504C6.38495 9.70317 6.1037 10.0125 6.13182 10.35L6.3287 12.825C6.35683 13.1625 6.63808 13.4157 6.94745 13.4157C6.97558 13.4157 6.97558 13.4157 7.0037 13.4157C7.3412 13.3875 7.62245 13.0782 7.59433 12.7407L7.39745 10.2657C7.39745 9.90004 7.08808 9.64692 6.72245 9.67504Z"/>
                                    </svg>
                                </button>
                            </form>
                        </div>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="5" class="px-4 py-8 text-center">
                        <p class="text-gray-500 dark:text-gray-400">
                            {% if search_query %}
                                No se encontraron usuarios que coincidan con "{{ search_query }}"
                            {% else %}
                                No hay usuarios registrados
                            {% endif %}
                        </p>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

<!-- Pagination -->
{% if users.has_other_pages %}
<div class="mt-6 flex flex-col items-center justify-between gap-4 md:flex-row">
    <!-- Info -->
    <span class="text-sm text-gray-500 dark:text-gray-400">
        Mostrando {{ users.start_index }} a {{ users.end_index }} de {{ users.paginator.count }} usuarios
    </span>
    
    <!-- Pagination Buttons -->
    <div class="flex gap-2">
        {% if users.has_previous %}
        <a href="?page={{ users.previous_page_number }}{% if search_query %}&q={{ search_query }}{% endif %}" 
           class="flex items-center justify-center rounded border border-gray-300 px-4 py-2 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700">
            <svg class="mr-2 fill-current" width="18" height="18" viewBox="0 0 18 18">
                <path d="M12.1777 16.1156C12.009 16.1156 11.8402 16.0593 11.7277 15.9187L5.37148 9.44995C5.11836 9.19683 5.11836 8.80308 5.37148 8.54995L11.7277 2.0812C11.9809 1.82808 12.3746 1.82808 12.6277 2.0812C12.8809 2.33433 12.8809 2.72808 12.6277 2.9812L6.72148 8.99995L12.6559 15.0187C12.909 15.2718 12.909 15.6656 12.6559 15.9187C12.5152 16.0312 12.3465 16.1156 12.1777 16.1156Z"/>
            </svg>
            Anterior
        </a>
        {% endif %}
        
        <!-- Page Numbers -->
        {% for num in users.paginator.page_range %}
            {% if num == users.number %}
            <span class="flex items-center justify-center rounded bg-primary px-4 py-2 text-white">
                {{ num }}
            </span>
            {% elif num > users.number|add:'-3' and num < users.number|add:'3' %}
            <a href="?page={{ num }}{% if search_query %}&q={{ search_query }}{% endif %}" 
               class="flex items-center justify-center rounded border border-gray-300 px-4 py-2 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700">
                {{ num }}
            </a>
            {% endif %}
        {% endfor %}
        
        {% if users.has_next %}
        <a href="?page={{ users.next_page_number }}{% if search_query %}&q={{ search_query }}{% endif %}" 
           class="flex items-center justify-center rounded border border-gray-300 px-4 py-2 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700">
            Siguiente
            <svg class="ml-2 fill-current" width="18" height="18" viewBox="0 0 18 18">
                <path d="M5.82148 16.1156C5.65273 16.1156 5.51211 16.0593 5.37148 15.9468C5.11836 15.6937 5.11836 15.3 5.37148 15.0468L11.2777 9.0562L5.37148 3.0374C5.11836 2.78428 5.11836 2.39053 5.37148 2.13741C5.62461 1.88428 6.01836 1.88428 6.27148 2.13741L12.6277 8.60616C12.8809 8.85928 12.8809 9.25303 12.6277 9.50616L6.27148 15.9749C6.15898 16.0874 5.99023 16.1156 5.82148 16.1156Z"/>
            </svg>
        </a>
        {% endif %}
    </div>
</div>
{% endif %}

{% endblock %}
```

Este manual ahora está completo con todos los ejemplos prácticos. ¿Quieres que continúe con más ejemplos o ajustes?

---

**Última actualización:** 2025-10-02
**Versión:** 1.0
**Autor:** Equipo J250929D_SAAS
