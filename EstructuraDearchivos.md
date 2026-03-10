Claro. Aquí tienes el desglose detallado de la arquitectura final del proyecto, explicando el propósito de cada uno de los 27 archivos, incluyendo los que están vacíos.

-----

## Arquitectura Detallada del Proyecto (27 Archivos)

```
.
├── actions/
│   ├── __init__.py
│   ├── custom_ask_affirmation.py
│   └── tramites/
│       ├── __init__.py
│       ├── components/
│       │   ├── __init__.py
│       │   └── validate_identity_form.py
│       ├── residencia_individual/
│       │   ├── __init__.py
│       │   └── residencia_individual.py
│       └── residencia_grupal/
│           ├── __init__.py
│           └── residencia_grupal.py
├── data/
│   ├── global/
│   │   ├── nlu_global.yml
│   │   ├── rules_global.yml
│   │   └── stories_global.yml
│   └── tramites/
│       ├── common_components/
│       │   ├── nlu_identity.yml
│       │   └── story_identity_validation.yml
│       ├── residencia_individual/
│       │   └── story_residencia_individual.yml
│       └── residencia_grupal/
│           └── story_residencia_grupal.yml
├── domain/
│   ├── core/
│   │   └── domain_core.yml
│   ├── components/
│   │   └── form_identity_validation.yml
│   └── tramites/
│       ├── residencia_individual.yml
│       └── residencia_grupal.yml
├── js/
│   └── rasa-webchat.js
├── config.yml
├── credentials.yml
├── docker-compose.yml
├── endpoints.yml
└── index.html
```

-----

## Descripción de Archivos

### Archivos de Configuración y Raíz (5 archivos)

1.  **`config.yml`**: El ADN del bot. Define el pipeline de NLU (cómo entiende el lenguaje) y las políticas de diálogo (cómo decide qué hacer), incluyendo nuestra estrategia de fallback unificado.
2.  **`credentials.yml`**: El "llavero" del bot. Define las credenciales para los canales de comunicación externos, como los canales `rest` y `socketio` que necesita nuestra interfaz web.
3.  **`docker-compose.yml`**: El plano maestro para orquestar los servicios. Define cómo se construyen y se comunican los contenedores de `rasa_server` y `action_server`.
4.  **`endpoints.yml`**: La "agenda de contactos". Le dice al `rasa_server` la dirección del `action_server` para que pueda ejecutar el código Python personalizado.
5.  **`index.html`**: Nuestra interfaz de chat web personalizada. Contiene el HTML, CSS y JavaScript para interactuar con el bot desde un navegador.

### Paquete de Acciones (`actions/`) (10 archivos)

La carpeta que contiene todo el código Python que ejecuta la lógica de negocio.

6.  **`actions/__init__.py`**: (Vacío) Su única función es decirle a Python que la carpeta `actions` es un "paquete", permitiendo que importemos código de forma ordenada.
7.  **`actions/custom_ask_affirmation.py`**: Contiene la lógica de nuestro fallback inteligente, incluyendo el evento `UserUtteranceReverted` para evitar bucles.
8.  **`actions/tramites/__init__.py`**: (Vacío) Convierte la carpeta `tramites` en un sub-paquete de Python.
9.  **`actions/tramites/components/__init__.py`**: (Vacío) Convierte la carpeta `components` en un sub-paquete de Python.
10. **`actions/tramites/components/validate_identity_form.py`**: Contiene la lógica de validación reutilizable para el formulario de identidad (ej. el algoritmo para validar una cédula).
11. **`actions/tramites/residencia_individual/__init__.py`**: (Vacío) Define el módulo del trámite individual.
12. **`actions/tramites/residencia_individual/residencia_individual.py`**: Contiene la acción orquestadora que guía al usuario a través del trámite de residencia individual.
13. **`actions/tramites/residencia_grupal/__init__.py`**: (Vacío) Define el módulo del trámite grupal.
14. **`actions/tramites/residencia_grupal/residencia_grupal.py`**: Contiene la acción orquestadora para el trámite de residencia grupal, manejando el bucle de validación de múltiples miembros.

### Paquete de Datos de Entrenamiento (`data/`) (7 archivos)

La carpeta que enseña al bot a entender y a conversar.

15. **`data/global/nlu_global.yml`**: El diccionario del bot. Contiene los ejemplos de intenciones y entidades globales (saludos, despedidas, apodos, etc.).
16. **`data/global/rules_global.yml`**: El libro de reglas del bot. Define comportamientos fijos e ineludibles, como qué hacer al saludar o cuando se activa el fallback.
17. **`data/global/stories_global.yml`**: El libro de guiones del bot. Contiene ejemplos de conversaciones fluidas para que el bot aprenda a seguirlas.
18. **`data/tramites/common_components/nlu_identity.yml`**: Define las formas en que un usuario puede proporcionar su cédula.
19. **`data/tramites/common_components/story_identity_validation.yml`**: Describe el flujo interno de cómo funciona el formulario de validación de identidad.
20. **`data/tramites/residencia_individual/story_residencia_individual.yml`**: El guion específico para el trámite de residencia individual.
21. **`data/tramites/residencia_grupal/story_residencia_grupal.yml`**: El guion específico para el trámite de residencia grupal.

### Paquete de Dominio (`domain/`) (4 archivos)

La carpeta que define todo el "vocabulario" y las capacidades del bot.

22. **`domain/core/domain_core.yml`**: La "constitución" del bot. Declara todas las intenciones, entidades, slots, respuestas y acciones que son compartidas por todo el proyecto.
23. **`domain/components/form_identity_validation.yml`**: Define la estructura del formulario reutilizable `identity_validation_form` y los slots que requiere.
24. **`domain/tramites/residencia_individual.yml`**: Define los elementos de dominio **únicos** para el trámite de residencia individual.
25. **`domain/tramites/residencia_grupal.yml`**: Define los elementos de dominio **únicos** para el trámite de residencia grupal (ej. `slot_grupo_tramite`).

### Archivos de Interfaz Web (2 archivos)

26. **`js/rasa-webchat.js`**: (Archivo descargado) Es el código de la librería del widget de chat que decidimos alojar localmente para evitar problemas de conexión con servidores externos.
27. **`index.html`**: La página web que aloja nuestro chat personalizado. La versión final utiliza una interfaz simple creada con JavaScript para comunicarse directamente con la API REST del bot.