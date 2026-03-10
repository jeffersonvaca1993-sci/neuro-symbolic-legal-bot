from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

class ResidenciaGrupal(Action):
    """
    Acción orquestadora para el trámite de residencia grupal.
    Gestiona el ciclo de vida completo del trámite, desde la
    recolección del número de miembros hasta la validación de cada uno.
    """

    def name(self) -> Text:
        return "residencia_grupal"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # --- 1. Obtener el estado actual de la conversación desde los slots ---
        numero_de_miembros = tracker.get_slot("numero_de_miembros")
        grupo_tramite = tracker.get_slot("slot_grupo_tramite")
        cedula_recien_validada = tracker.get_slot("cedula_ec")
        miembro_actual_index = tracker.get_slot("miembro_actual_index")

        # Lista de eventos a retornar al final
        events: List[Dict[Text, Any]] = []

        # --- 2. Si no sabemos cuántos miembros son, preguntar primero ---
        if numero_de_miembros is None:
            dispatcher.utter_message(response="utter_ask_numero_de_miembros")
            return []

        # --- 3. Si el grupo no ha sido creado, inicializarlo ---
        # Esto ocurre una sola vez, justo después de que el usuario indica el número de miembros.
        if grupo_tramite is None:
            num_miembros_int = int(numero_de_miembros)
            # Creamos la lista de diccionarios, uno para cada miembro del grupo.
            grupo_tramite = [
                {
                    "id_interno": i + 1,
                    "cedula": None,
                    "estado_validacion": "pendiente",
                }
                for i in range(num_miembros_int)
            ]
            events.append(SlotSet("slot_grupo_tramite", grupo_tramite))
            dispatcher.utter_message(response="utter_start_grupo", numero_de_miembros=num_miembros_int)

        # --- 4. Si una cédula acaba de ser validada, actualizar el grupo ---
        # El formulario 'identity_validation_form' guarda la cédula en 'cedula_ec'.
        # Aquí la recogemos y la guardamos en nuestro contenedor principal 'slot_grupo_tramite'.
        if cedula_recien_validada and miembro_actual_index is not None:
            for miembro in grupo_tramite:
                if miembro["id_interno"] == miembro_actual_index:
                    miembro["cedula"] = cedula_recien_validada
                    miembro["estado_validacion"] = "validado"
                    break  # Salimos del bucle una vez encontrado y actualizado

            # Actualizamos el contenedor principal y limpiamos el slot temporal 'cedula_ec'.
            events.extend([
                SlotSet("slot_grupo_tramite", grupo_tramite),
                SlotSet("cedula_ec", None),
            ])

        # --- 5. Buscar al siguiente miembro pendiente para validar ---
        siguiente_miembro_a_validar = None
        for miembro in grupo_tramite:
            if miembro["estado_validacion"] == "pendiente":
                siguiente_miembro_a_validar = miembro
                break

        # --- 6. Si encontramos un miembro pendiente, iniciar su validación ---
        if siguiente_miembro_a_validar:
            indice_actual = siguiente_miembro_a_validar["id_interno"]
            events.append(SlotSet("miembro_actual_index", indice_actual))
            dispatcher.utter_message(
                response="utter_ask_for_next_member", miembro_actual_index=indice_actual
            )
            # Activamos el formulario reutilizable para que haga su trabajo.
            events.append(FollowupAction("identity_validation_form"))
            return events

        # --- 7. Si no hay miembros pendientes, el trámite ha finalizado ---
        else:
            dispatcher.utter_message(
                response="utter_confirmacion_tramite_grupal",
                numero_de_miembros=int(numero_de_miembros),
            )
            # Limpiamos TODOS los slots relacionados con este trámite para evitar
            # problemas de memoria en futuras conversaciones.
            events.extend([
                SlotSet("numero_de_miembros", None),
                SlotSet("miembro_actual_index", None),
                SlotSet("slot_grupo_tramite", None),
                SlotSet("slot_tramite_type", None), # Crucial para permitir nuevos trámites
            ])
            # Preguntamos al usuario si desea hacer algo más.
            events.append(FollowupAction("utter_what_else"))
            return events