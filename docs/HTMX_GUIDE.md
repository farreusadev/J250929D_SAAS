# Guía de HTMX + Alpine.js para Django

## Introducción

Este proyecto utiliza **HTMX** para interacciones dinámicas y **Alpine.js** para reactividad del lado del cliente, todo integrado con Django.

### Stack Frontend
- **Tailwind CSS v4** - Estilos utility-first
- **Alpine.js v3.14** - Reactividad ligera del cliente
- **HTMX v1.9.10** - Interacciones AJAX sin JavaScript
- **TailAdmin Pro** - Componentes UI pre-diseñados

---

## HTMX Básico

### 1. Cargar Contenido Dinámicamente

```html
<!-- Button que carga contenido -->
<button 
    hx-get="/api/users" 
    hx-target="#user-list" 
    hx-swap="innerHTML"
    class="btn btn-primary"
>
    Cargar Usuarios
</button>

<div id="user-list">
    <!-- El contenido se cargará aquí -->
</div>
```

### 2. Formularios con HTMX

```html
<form 
    hx-post="{% url 'users:create' %}" 
    hx-target="#user-list"
    hx-swap="beforeend"
>
    {% csrf_token %}
    <input type="text" name="name" placeholder="Nombre" required>
    <input type="email" name="email" placeholder="Email" required>
    <button type="submit">Crear Usuario</button>
</form>
```

### 3. Confirmación antes de Eliminar

```html
<button 
    hx-delete="{% url 'users:delete' user.id %}"
    hx-confirm="¿Estás seguro de eliminar este usuario?"
    hx-target="closest tr"
    hx-swap="outerHTML swap:1s"
    class="btn btn-danger"
>
    Eliminar
</button>
```

### 4. Indicador de Carga

```html
<button 
    hx-get="/api/data" 
    hx-target="#content"
    hx-indicator="#spinner"
>
    Cargar Datos
</button>

<div id="spinner" class="htmx-indicator">
    <div class="spinner"></div>
</div>

<style>
.htmx-indicator {
    display: none;
}
.htmx-request .htmx-indicator {
    display: inline-block;
}
</style>
```

---

## Alpine.js + HTMX

### Combinar Alpine.js con HTMX

```html
<div x-data="{ open: false, count: 0 }">
    <!-- Alpine.js controla el estado local -->
    <button @click="open = !open">
        Toggle Panel
    </button>
    
    <!-- HTMX maneja la comunicación con el servidor -->
    <button 
        hx-post="/api/increment"
        hx-vals='{"current": count}'
        @htmx:after-request="count++"
    >
        Incrementar en Servidor
    </button>
    
    <div x-show="open">
        Count: <span x-text="count"></span>
    </div>
</div>
```

### Eventos HTMX en Alpine.js

```html
<div 
    x-data="{ loading: false, error: null }"
    @htmx:before-request="loading = true"
    @htmx:after-request="loading = false"
    @htmx:response-error="error = $event.detail.error"
>
    <button hx-get="/api/data" hx-target="#result">
        Cargar
    </button>
    
    <div x-show="loading">Cargando...</div>
    <div x-show="error" x-text="error"></div>
    <div id="result"></div>
</div>
```

---

## Patrones Comunes en Django

### 1. Tabla con Paginación

**Template (users/list.html):**
```html
{% extends 'base.html' %}

{% block content %}
<div class="rounded-lg border border-gray-200 bg-white p-6">
    <h2 class="text-xl font-semibold mb-4">Usuarios</h2>
    
    <div id="users-table">
        {% include 'users/_table.html' %}
    </div>
</div>
{% endblock %}
```

**Partial (_table.html):**
```html
<table class="w-full">
    <thead>
        <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
        <tr id="user-{{ user.id }}">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>
                <button 
                    hx-delete="{% url 'users:delete' user.id %}"
                    hx-target="#user-{{ user.id }}"
                    hx-swap="outerHTML swap:1s"
                    hx-confirm="¿Eliminar usuario?"
                >
                    Eliminar
                </button>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<!-- Paginación -->
<div class="mt-4 flex justify-between">
    {% if page_obj.has_previous %}
    <button 
        hx-get="?page={{ page_obj.previous_page_number }}"
        hx-target="#users-table"
        hx-swap="innerHTML"
    >
        Anterior
    </button>
    {% endif %}
    
    {% if page_obj.has_next %}
    <button 
        hx-get="?page={{ page_obj.next_page_number }}"
        hx-target="#users-table"
        hx-swap="innerHTML"
    >
        Siguiente
    </button>
    {% endif %}
</div>
```

**View (views.py):**
```python
from django.shortcuts import render
from django.core.paginator import Paginator

def user_list(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    # Si es request HTMX, devolver solo el partial
    if request.headers.get('HX-Request'):
        return render(request, 'users/_table.html', {'users': page_obj, 'page_obj': page_obj})
    
    # Si no, devolver página completa
    return render(request, 'users/list.html', {'users': page_obj, 'page_obj': page_obj})
```

### 2. Modal con Formulario

**Template:**
```html
<button 
    hx-get="{% url 'users:create_form' %}"
    hx-target="#modal-container"
    @click="$dispatch('open-modal')"
>
    Nuevo Usuario
</button>

<div 
    id="modal-container"
    x-data="{ open: false }"
    @open-modal.window="open = true"
    @close-modal.window="open = false"
    x-show="open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    style="display: none;"
>
    <!-- El formulario se cargará aquí -->
</div>
```

**Partial (_form.html):**
```html
<div class="rounded-lg bg-white p-6 max-w-md">
    <h3 class="text-lg font-semibold mb-4">Crear Usuario</h3>
    
    <form 
        hx-post="{% url 'users:create' %}"
        hx-target="#users-table"
        hx-swap="afterbegin"
        @htmx:after-request="$dispatch('close-modal')"
    >
        {% csrf_token %}
        {{ form.as_p }}
        
        <div class="mt-4 flex gap-2">
            <button type="submit" class="btn btn-primary">
                Guardar
            </button>
            <button 
                type="button" 
                @click="$dispatch('close-modal')"
                class="btn btn-secondary"
            >
                Cancelar
            </button>
        </div>
    </form>
</div>
```

### 3. Búsqueda en Tiempo Real

```html
<input 
    type="search"
    name="q"
    placeholder="Buscar usuarios..."
    hx-get="{% url 'users:search' %}"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results"
    hx-indicator="#search-spinner"
>

<div id="search-spinner" class="htmx-indicator">
    Buscando...
</div>

<div id="search-results">
    <!-- Resultados aquí -->
</div>
```

**View:**
```python
def search_users(request):
    q = request.GET.get('q', '')
    users = User.objects.filter(name__icontains=q)[:10]
    return render(request, 'users/_search_results.html', {'users': users})
```

---

## Middleware Helper para HTMX

**middleware.py:**
```python
class HTMXMiddleware:
    """Middleware para facilitar detección de requests HTMX"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        request.htmx = request.headers.get('HX-Request') == 'true'
        request.htmx_trigger = request.headers.get('HX-Trigger')
        request.htmx_target = request.headers.get('HX-Target')
        return self.get_response(request)
```

**Uso en views:**
```python
def my_view(request):
    if request.htmx:
        # Devolver partial
        return render(request, 'partial.html', context)
    else:
        # Devolver página completa
        return render(request, 'full_page.html', context)
```

---

## Mejores Prácticas

### 1. Estructura de Templates

```
templates/
├── base.html
├── users/
│   ├── list.html           # Vista completa
│   ├── _table.html         # Partial para HTMX
│   ├── _form.html          # Partial para formularios
│   └── _search_results.html # Partial para búsqueda
```

### 2. Convención de Nombres

- Partials: prefijo `_`
- IDs únicos: `#entity-{id}` para targeting específico
- Targets: usar IDs descriptivos

### 3. CSRF Token

Siempre incluir en formularios HTMX:
```html
<form hx-post="/url">
    {% csrf_token %}
    <!-- campos -->
</form>
```

### 4. Mensajes de Éxito/Error

```python
from django.contrib import messages

def create_user(request):
    if request.method == 'POST':
        # ... crear usuario
        messages.success(request, 'Usuario creado exitosamente')
        return render(request, 'users/_row.html', {'user': user})
```

```html
<!-- En base.html -->
<div id="messages" hx-swap-oob="true">
    {% if messages %}
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
        {% endfor %}
    {% endif %}
</div>
```

---

## Eventos HTMX Útiles

```javascript
// Escuchar eventos HTMX
document.body.addEventListener('htmx:afterRequest', function(evt) {
    console.log('Request completado:', evt.detail);
});

document.body.addEventListener('htmx:responseError', function(evt) {
    console.error('Error:', evt.detail);
});
```

---

## Recursos

- **HTMX Docs:** https://htmx.org/docs/
- **Alpine.js Docs:** https://alpinejs.dev/
- **Ejemplos:** Ver `templates/dashboard.html` y componentes

---

## Testing

```python
from django.test import TestCase

class HTMXViewTest(TestCase):
    def test_htmx_request(self):
        response = self.client.get(
            '/users/',
            HTTP_HX_REQUEST='true'
        )
        # Debe devolver partial
        self.assertContains(response, '<table')
        self.assertNotContains(response, '<html')
```




