# Contenido para actions/tramites/residencia_individual/residencia_individual.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop

class ResidenciaIndividual(Action):
    def name(self) -> Text:
        return "residencia_individual"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        # Limpieza de slots de otros trámites para evitar contaminación
        events = [
            SlotSet("numero_de_miembros", None),
            SlotSet("miembro_actual_index", None),
            SlotSet("slot_grupo_tramite", None)
        ]

        dispatcher.utter_message(
            text="Iniciaremos el trámite de residencia individual. Primero, necesito validar su identidad."
        )
        
        events.append(ActiveLoop("identity_validation_form"))
        
        return events