# Contenido COMPLETO y CORREGIDO para actions/custom_ask_affirmation.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import UserUttered
# 1. AÑADIMOS EL IMPORT NECESARIO PARA ROMPER EL BUCLE
from rasa_sdk.events import UserUtteranceReverted

class CustomAskAffirmation(Action):
    def name(self) -> Text:
        return "custom_ask_affirmation"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:

        # --- LÓGICA 1: PROCESAMIENTO DE ARCHIVOS ADJUNTOS (se mantiene tu lógica) ---
        latest_message = tracker.latest_message
        if latest_message.get("attachments"):
            # Aquí iría tu lógica real de transcripción. Por ahora es una simulación.
            dispatcher.utter_message(text=f"He recibido un archivo, un momento mientras lo proceso.")
            texto_transcrito = "" # Simulación
            if texto_transcrito:
                return [UserUttered(texto_transcrito)]

        # --- LÓGICA 2: RECUPERACIÓN CONVERSACIONAL CONTEXTUAL CON LLM (se mantiene tu lógica) ---
        user_nickname = tracker.get_slot("slot_nickname") or "usted"
        last_user_message = latest_message.get("text")
        
        history = []
        for event in tracker.events[-10:]:
            if event.get("event") == "user":
                history.append(f"Usuario: {event.get('text')}")
            elif event.get("event") == "bot":
                history.append(f"Asistente: {event.get('text')}")
        detailed_context = "\n".join(history)

        # --- OBTENCIÓN DEL ESTADO ACTUAL DEL BOT (se mantiene tu lógica) ---
        active_form = tracker.active_loop.get('name')
        last_action = tracker.latest_action_name
        
        if active_form:
            contexto_actual_bot = f"El bot se encuentra actualmente llenando el formulario '{active_form}'."
        elif last_action:
            contexto_actual_bot = f"La última acción del bot fue '{last_action}'."
        else:
            contexto_actual_bot = "El bot está en un estado de conversación general."

        # --- CONSTRUCCIÓN DEL PROMPT CONTEXTUAL (se mantiene tu lógica) ---
        prompt = f"""
        Eres un asistente IA de un consultorio jurídico. Tu tono es profesional y demuestra escucha activa.
        Un usuario, a quien nos referimos como '{user_nickname}', ha enviado un mensaje que el sistema no pudo entender con certeza.

        HISTORIAL RECIENTE:
        {detailed_context}
        
        ESTADO ACTUAL DEL BOT:
        {contexto_actual_bot}

        MENSAJE CONFUSO DEL USUARIO: "{last_user_message}"

        TU MISIÓN:
        Basándote en el ESTADO ACTUAL del bot, genera una respuesta que:
        1.  Reconozca la consulta del usuario.
        2.  Lo reoriente suavemente hacia la tarea que el bot estaba intentando realizar (ej. llenar el formulario actual).
        3.  Si el estado es general, redirige a los trámites principales.
        """
        
        # TODO: Implementar la llamada real a la API del LLM (Gemma/Gemini).
        # llm_response_text = call_gemma_api(prompt)
        
        # Simulación de una respuesta de alta calidad del LLM:
        llm_response_text = (f"Entiendo que su consulta es sobre '{last_user_message}', {user_nickname}. "
                             f"Para poder asistirle correctamente, primero necesitamos completar el paso actual. "
                             f"¿Podríamos continuar con el trámite que estábamos realizando?")

        dispatcher.utter_message(text=llm_response_text)

        # 2. CAMBIAMOS EL RETURN PARA ROMPER EL BUCLE
        # Esto le dice al bot que ignore la última entrada del usuario y espere una nueva.
        return [UserUtteranceReverted()]