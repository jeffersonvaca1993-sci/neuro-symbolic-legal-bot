# Proyecto: Asistente Conversacional para Consultorio Jurídico

> [!IMPORTANT]
> ⚠️ **Estado del Proyecto: Prueba de Concepto (PoC) / Architecture Sandbox**
> Este repositorio no está diseñado como un producto final (Drop-in replacement) para producción inmediata. Funciona como un Laboratorio de Arquitectura donde se diseñaron y validaron paradigmas de ingeniería para sistemas de IA compuestos (Compound AI Systems).

**Versión:** 1.0
**Fecha:** 10 de julio de 2025

## 1. El Reto Arquitectónico

En entornos críticos como el sector jurídico, los Modelos de Lenguaje Grandes (LLMs) puros presentan un riesgo inaceptable debido a las "alucinaciones" y su incapacidad para garantizar el cumplimiento estricto de procesos transaccionales (ej. validación de identidad obligatoria antes de un trámite).

El objetivo de este diseño es validar una Arquitectura Neuro-Simbólica capaz de:

* Garantizar cero alucinaciones en la ruta crítica mediante enrutamiento determinista.
* Mantener una experiencia de usuario empática y flexible delegando el manejo de excepciones a IA Generativa.
* Orquestar automatizaciones de backend (generación de expedientes) de forma asíncrona.

## 2. Paradigma de Diseño: Sistema Híbrido y Desacoplado

El sistema se basa en una separación estricta de responsabilidades, donde cada componente cumple un rol especializado:

* **El Núcleo Determinista (Rasa Open Source):** Actúa como el cerebro transaccional (DIETClassifier, RulePolicy). Su responsabilidad exclusiva es entender la intención principal, extraer entidades clave (cédulas, nombres), mantener la máquina de estados y forzar la ejecución de la lógica de negocio sin desviaciones.
* **El Fallback Inteligente (Gemma / LLM Injection):** El LLM no controla la conversación. Se utiliza como un "Especialista Lingüístico" de rescate. Cuando el NLU de Rasa detecta baja confianza (ambigüedad), inyecta el contexto de la sesión al LLM para que este genere una respuesta empática que redirija al usuario suavemente hacia el flujo estricto (Error Recovery).
* **Persistencia de Estado (External DB):** Almacenamiento del estado de los trámites, permitiendo pausar y reanudar flujos complejos entre sesiones (resiliencia de sesión).
* **Motor de Procesos (n8n):** Activado mediante webhooks asíncronos desde el Action Server para orquestar tareas pesadas de backend que no requieren bloqueo de la interfaz de usuario (ej. creación de PDFs, envíos de correo).

## 3. Modularidad en la Capa de Lógica (Action Server)

El corazón técnico de la escalabilidad de este proyecto reside en su arquitectura de software modular para las acciones personalizadas:

* **Principio de Diseño:** Agrupación por Funcionalidad de Negocio (Trámite), no por Tipo de Archivo.
* **Orquestadores (`actions/tramites/<tramite>.py`):** Cada servicio legal posee una acción principal que actúa como director. Contiene la "receta" estricta de pasos requeridos.
* **Componentes Reutilizables (`actions/tramites/components/`):** Tareas comunes (como la validación criptográfica o de formato de una cédula de identidad) se encapsulan en formularios y acciones atómicas. Los orquestadores invocan estos componentes evitando la duplicación de código (ej. un trámite de residencia grupal invoca el validador de identidad iterativamente en un bucle).

## 4. Gestión del Flujo Conversacional (State Machine)

La experiencia del usuario se modeló como un ciclo transaccional continuo:

* **Soft Onboarding:** Saludo y petición opcional de apodo para reducir la fricción inicial.
* **Centro de Mando (Routing):** Presentación proactiva de servicios. Bifurcación entre el Modo Informativo (RAG/FAQ sin estado) y el Modo Transaccional (ejecución de Forms estrictos).
* **Retención de Ciclo:** Al finalizar un trámite, la máquina de estados no finaliza la sesión abruptamente, sino que re-enruta al "Centro de Mando" para incentivar transacciones múltiples en la misma sesión.

---
# El entrenamiento se realiza con 

docker-compose run --rm rasa data validate --domain domain