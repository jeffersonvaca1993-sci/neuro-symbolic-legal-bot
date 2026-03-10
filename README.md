De acuerdo. Aquí tiene un archivo `README.md` que detalla los objetivos y la lógica de la arquitectura completa que hemos diseñado. Este documento puede servir como la memoria técnica y el plano maestro de su proyecto.

---
# Proyecto: Asistente Conversacional para Consultorio Jurídico

**Versión:** 1.0
**Fecha:** 10 de julio de 2025

## 1. Objetivo del Proyecto

El objetivo principal de este proyecto es construir un asistente conversacional avanzado y escalable para un consultorio jurídico. El asistente está diseñado para cumplir dos funciones estratégicas:

1.  **Optimizar la Interacción con el Cliente (Fase 1):** Ofrecer un canal de comunicación eficiente y amigable, capaz de recolectar información, validar datos de identidad y guiar a los usuarios a través de los servicios ofrecidos, manteniendo siempre un tono profesional y personalizado.
2.  **Automatizar Procesos Internos (Fase 2):** Servir como el punto de entrada para flujos de trabajo de backend (orquestados por n8n), como la generación de expedientes, la redacción de documentos y el envío de notificaciones, basándose en la información recolectada durante la conversación.

## 2. Arquitectura General

El sistema se basa en una arquitectura híbrida y desacoplada, donde cada herramienta cumple un rol especializado:

* **Rasa Open Source (El Núcleo Conversacional):** Actúa como el cerebro principal que gestiona el flujo del diálogo. Su responsabilidad es entender la intención del usuario, mantener el estado de la conversación y ejecutar la lógica de negocio inmediata.
* **Gemma/LLM (El Experto Lingüístico):** No controla la conversación, sino que es un especialista consultado por Rasa para tareas específicas que requieren generación de lenguaje natural avanzado. Su rol principal en esta arquitectura es el **Fallback Inteligente**, donde genera respuestas empáticas y contextuales cuando el bot no entiende al usuario.
* **Base de Datos Externa (La Memoria a Largo Plazo):** Un componente crucial para la persistencia. Almacena el estado de los trámites, permitiendo a los usuarios pausar y reanudar procesos complejos entre sesiones y al bot consultar el estado de un trámite en curso.
* **n8n (El Motor de Procesos de Backend):** Se activa mediante webhooks desde Rasa para orquestar tareas asíncronas y complejas que no requieren interacción directa con el usuario (ej. crear un PDF, enviar 5 correos, actualizar un CRM).

## 3. Lógica de la Conversación (El Flujo del Usuario)

La experiencia del usuario está diseñada para ser fluida, cíclica y respetuosa, operando en dos modos principales.

1.  **Bienvenida y Personalización:** Toda conversación inicia con un saludo y una petición **opcional** de un apodo. Esto establece un tono amigable desde el primer momento sin crear una barrera para el usuario.
2.  **Menú de Servicios (El Centro de Mando):** Inmediatamente después, el bot presenta proactivamente los servicios disponibles mediante botones. En este punto, el usuario puede entrar en:
    * **Modo Informativo:** Realizar preguntas generales (`ask_general_info`) sin necesidad de identificarse.
    * **Modo Transaccional:** Seleccionar un trámite específico (`request_service`).
3.  **Ejecución de un Trámite:** Al seleccionar un trámite, se activa la lógica de negocio correspondiente. Es aquí donde se solicita la información obligatoria (como la cédula).
4.  **Ciclo Conversacional:** Una vez finalizado un trámite o una consulta, el bot no termina la conversación, sino que vuelve al "Centro de Mando", preguntando proactivamente "¿En qué más puedo ayudarle?" y mostrando de nuevo las opciones. Esto permite al usuario realizar múltiples trámites para sí mismo o para otros en una sola sesión.

## 4. El Paradigma de Diseño: Arquitectura Modular

El corazón técnico del proyecto es su arquitectura de software modular, aplicada a los datos, la lógica de acciones y el dominio.

* **Principio:** Agrupación por **Funcionalidad (Trámite)**, no por Tipo de Archivo.
* **Orquestadores (`actions/tramites/<tramite>.py`):** Cada servicio (ej. `residencia_grupal`) tiene una acción principal en Python que actúa como "director de orquesta". Esta acción contiene la "receta" única de pasos para ese trámite.
* **Componentes Reutilizables (`actions/tramites/components/`):** Tareas comunes, como la validación de una cédula, se encapsulan en sus propios formularios y acciones. Los orquestadores pueden llamar a estos componentes según sea necesario, evitando la duplicación de código. Por ejemplo, el orquestador `residencia_grupal` llama al componente `identity_validation_form` varias veces dentro de un bucle.
* **Estructura de Archivos Consistente:** Las carpetas `data`, `domain` y `actions` siguen esta misma estructura modular, haciendo que añadir, modificar o depurar un trámite sea un proceso aislado y seguro.

## 5. Manejo de Errores y Flexibilidad

El sistema está diseñado para ser robusto y manejar la incertidumbre.

* **Fallback Inteligente:** Cuando el NLU de Rasa no entiende al usuario con suficiente confianza, no da una respuesta genérica. En su lugar, se activa una regla que llama a la acción `custom_ask_affirmation`. Esta acción:
    1.  Recolecta el contexto completo de la conversación (historial, formulario activo).
    2.  Envía este contexto a Gemma/LLM con la misión de generar una respuesta empática.
    3.  La respuesta de Gemma reconoce la posible intención del usuario y lo redirige suavemente a la tarea que el bot estaba intentando realizar, creando una recuperación de errores muy natural.
* **Pausa y Reanudación (Habilitado por Diseño):** La arquitectura con una base de datos externa permite implementar fácilmente la capacidad de pausar trámites largos (ej. si un usuario no tiene un documento a mano) y reanudarlos más tarde, incluso en una sesión diferente, ya que el estado se conserva en la base de datos y no solo en la memoria del bot.


# El entrenamiento se realiza con 

docker-compose run --rm rasa data validate --domain domain