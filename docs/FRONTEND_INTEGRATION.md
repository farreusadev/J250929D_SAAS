# Integración Frontend - Django + TailAdmin + HTMX + Alpine.js

## Stack Completo

```
Frontend Stack:
├── Tailwind CSS v4       → Estilos
├── Alpine.js v3.14       → Reactividad cliente
├── HTMX v1.9.10         → AJAX sin JavaScript
└── TailAdmin Pro v2.0   → Componentes UI
```

---

## Arquitectura

### Flujo de Datos

```
Usuario → Interacción
    ↓
Alpine.js (Estado Local)
    ↓
HTMX (Comunicación Servidor)
    ↓
Django View
    ↓
Template Partial (Response)
    ↓
DOM Update (HTMX)
```

---

## Cuándo Usar Cada Tecnología

### Alpine.js
**Usar para:**
- ✅ Estado local del componente
- ✅ Toggles, dropdowns, modals
- ✅ Validación del lado del cliente
- ✅ Animaciones y transiciones
- ✅ Dark mode, preferencias locales

**Ejemplo:**
```html
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open">Contenido</div>
</div>
```

### HTMX
**Usar para:**
- ✅ Cargar contenido del servidor
- ✅ Formularios AJAX
- ✅ Paginación
- ✅ Búsqueda en tiempo real
- ✅ CRUD operations

**Ejemplo:**
```html
<button 
    hx-get="/api/data" 
    hx-target="#result"
>
    Cargar
</button>
```

### Tailwind CSS
**Usar para:**
- ✅ Todos los estilos
- ✅ Responsive design
- ✅ Dark mode
- ✅ Custom components

**Ejemplo:**
```html
<div class="rounded-lg bg-white p-6 shadow-md dark:bg-gray-900">
    Content
</div>
```

---

## Patrones de Integración

### 1. Component con Estado + HTMX

```html
<div 
    x-data="{ 
        loading: false, 
        error: null,
        data: [] 
    }"
    @htmx:before-request="loading = true"
    @htmx:after-request="loading = false; data = JSON.parse($event.detail.xhr.response)"
    @htmx:response-error="error = 'Error al cargar datos'"
>
    <!-- Button con HTMX -->
    <button 
        hx-get="/api/users"
        hx-target="#user-list"
        :disabled="loading"
    >
        <span x-show="!loading">Cargar Usuarios</span>
        <span x-show="loading">Cargando...</span>
    </button>
    
    <!-- Error message con Alpine -->
    <div x-show="error" x-text="error" class="text-error-500"></div>
    
    <!-- Results -->
    <div id="user-list"></div>
</div>
```

### 2. Form Validation + HTMX Submit

```html
<form 
    x-data="{ 
        name: '',
        email: '',
        errors: {} 
    }"
    @submit.prevent="
        errors = {};
        if (!name) errors.name = 'Nombre requerido';
        if (!email) errors.email = 'Email requerido';
        if (Object.keys(errors).length === 0) {
            $el.dispatchEvent(new Event('submit', { bubbles: true }));
        }
    "
    hx-post="{% url 'users:create' %}"
    hx-target="#user-list"
    hx-swap="afterbegin"
>
    {% csrf_token %}
    
    <div>
        <input 
            type="text" 
            name="name" 
            x-model="name"
            placeholder="Nombre"
        >
        <span x-show="errors.name" x-text="errors.name" class="text-error-500"></span>
    </div>
    
    <div>
        <input 
            type="email" 
            name="email" 
            x-model="email"
            placeholder="Email"
        >
        <span x-show="errors.email" x-text="errors.email" class="text-error-500"></span>
    </div>
    
    <button type="submit">Guardar</button>
</form>
```

### 3. Modal Dinámico

```html
<!-- Modal Component con Alpine + HTMX -->
<div x-data="{ open: false, content: '' }">
    <!-- Trigger -->
    <button 
        @click="open = true"
        hx-get="{% url 'users:form' %}"
        hx-target="#modal-content"
    >
        Nuevo Usuario
    </button>
    
    <!-- Modal -->
    <div 
        x-show="open"
        x-transition.opacity
        @keydown.escape.window="open = false"
        @close-modal.window="open = false"
        class="fixed inset-0 z-999 flex items-center justify-center bg-black/50"
        style="display: none;"
    >
        <div 
            @click.away="open = false"
            class="rounded-lg bg-white p-6 max-w-lg w-full"
        >
            <div id="modal-content">
                <!-- HTMX carga el contenido aquí -->
            </div>
        </div>
    </div>
</div>
```

### 4. Infinite Scroll

```html
<div x-data="{ page: 1 }">
    <div id="items-container">
        <!-- Items aquí -->
    </div>
    
    <div 
        x-intersect="
            page++;
            $el.querySelector('button').click();
        "
    >
        <button 
            hx-get="/api/items"
            :hx-vals=`{"page": ${page}}`
            hx-target="#items-container"
            hx-swap="beforeend"
            style="display:none;"
        ></button>
        
        <div class="text-center">Cargando más...</div>
    </div>
</div>
```

### 5. Search con Debounce

```html
<div x-data="{ query: '', results: [] }">
    <input 
        type="search"
        x-model="query"
        @input.debounce.500ms="
            if (query.length > 2) {
                $el.closest('div').querySelector('[hx-get]').click();
            }
        "
        placeholder="Buscar..."
    >
    
    <button 
        hx-get="/api/search"
        :hx-vals=`{"q": "${query}"}`
        hx-target="#search-results"
        style="display:none;"
    ></button>
    
    <div id="search-results"></div>
</div>
```

---

## Componentes Reutilizables

### Button con Loading State

```html
<!-- components/button_loading.html -->
<button 
    x-data="{ loading: false }"
    @htmx:before-request="loading = true"
    @htmx:after-request="loading = false"
    :disabled="loading"
    {{ attributes }}
>
    <span x-show="!loading">{{ label }}</span>
    <span x-show="loading" class="flex items-center gap-2">
        <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Cargando...
    </span>
</button>
```

### Toast Notifications

```html
<!-- components/toast.html -->
<div 
    x-data="{ 
        show: false, 
        message: '', 
        type: 'success' 
    }"
    @show-toast.window="
        show = true;
        message = $event.detail.message;
        type = $event.detail.type || 'success';
        setTimeout(() => show = false, 3000);
    "
    x-show="show"
    x-transition
    class="fixed top-4 right-4 z-99999 rounded-lg p-4 shadow-lg"
    :class="{
        'bg-success-500 text-white': type === 'success',
        'bg-error-500 text-white': type === 'error',
        'bg-warning-500 text-white': type === 'warning'
    }"
    style="display: none;"
>
    <p x-text="message"></p>
</div>

<!-- Usar en cualquier lugar -->
<script>
window.showToast = (message, type = 'success') => {
    window.dispatchEvent(new CustomEvent('show-toast', {
        detail: { message, type }
    }));
};
</script>
```

### Confirm Dialog

```html
<!-- components/confirm.html -->
<div 
    x-data="{ 
        show: false, 
        message: '', 
        callback: null 
    }"
    @confirm.window="
        show = true;
        message = $event.detail.message;
        callback = $event.detail.callback;
    "
    x-show="show"
    class="fixed inset-0 z-99999 flex items-center justify-center bg-black/50"
    style="display: none;"
>
    <div class="rounded-lg bg-white p-6 max-w-sm">
        <p x-text="message" class="mb-4"></p>
        <div class="flex gap-2">
            <button 
                @click="callback(); show = false;"
                class="btn btn-primary"
            >
                Confirmar
            </button>
            <button 
                @click="show = false"
                class="btn btn-secondary"
            >
                Cancelar
            </button>
        </div>
    </div>
</div>
```

---

## Optimizaciones

### 1. Preload de Contenido

```html
<div 
    hx-get="/api/content"
    hx-trigger="load"
    hx-target="this"
>
    <div class="animate-pulse">Cargando...</div>
</div>
```

### 2. Prefetch al Hover

```html
<a 
    href="/page"
    hx-get="/page"
    hx-trigger="mouseenter once"
    hx-swap="none"
>
    Link (prefetch on hover)
</a>
```

### 3. Lazy Loading de Imágenes

```html
<img 
    data-src="image.jpg"
    x-intersect="$el.src = $el.dataset.src"
    alt="Lazy loaded image"
>
```

---

## Debug y Development

### HTMX Debug

```html
<!-- Activar debug en desarrollo -->
<script>
htmx.logger = function(elt, event, data) {
    if(console) {
        console.log('HTMX:', event, data);
    }
}
</script>
```

### Alpine Debug

```html
<!-- Ver estado de Alpine -->
<div x-data="{ count: 0 }">
    <button @click="count++">Increment</button>
    <pre x-text="JSON.stringify($data, null, 2)"></pre>
</div>
```

---

## Mejores Prácticas

1. **Separación de Responsabilidades**
   - Alpine.js: UI state
   - HTMX: Server communication
   - Tailwind: Styling

2. **Progressive Enhancement**
   - Aplicación funciona sin JS
   - HTMX mejora la experiencia
   - Alpine añade interactividad

3. **Performance**
   - Usar `hx-trigger="revealed"` para lazy load
   - Debounce en búsquedas
   - Prefetch contenido probable

4. **Accesibilidad**
   - Mantener formularios funcionales sin JS
   - ARIA labels apropiados
   - Focus management en modals

---

## Referencias

- **Tailwind CSS:** https://tailwindcss.com
- **Alpine.js:** https://alpinejs.dev
- **HTMX:** https://htmx.org
- **TailAdmin:** https://tailadmin.com

