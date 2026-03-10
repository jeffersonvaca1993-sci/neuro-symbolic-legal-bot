# Contenido para actions/tramites/components/validate_identity_form.py

from typing import Any, Text, Dict, List
import re
from rasa_sdk import FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

# Se asume que esta función de validación está disponible.
def validar_cedula_ecuatoriana(cedula: str) -> bool:
    if not cedula.isdigit() or len(cedula) != 10:
        return False
    codigo_provincia = int(cedula[0:2])
    if not (1 <= codigo_provincia <= 24):
        return False
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    digito_verificador_real = int(cedula[9])
    suma = 0
    for i in range(9):
        digito = int(cedula[i])
        producto = digito * coeficientes[i]
        if producto >= 10:
            producto -= 9
        suma += producto
    residuo = suma % 10
    if residuo == 0:
        digito_verificador_calculado = 0
    else:
        digito_verificador_calculado = 10 - residuo
    return digito_verificador_calculado == digito_verificador_real


class ValidateIdentityForm(FormValidationAction):
    """Valida la información recolectada por el 'identity_validation_form'."""

    def name(self) -> Text:
        """
        Nombre único de la acción de validación.
        Debe ser 'validate_' + nombre del formulario ('identity_validation_form').
        """
        return "validate_identity_validation_form"

    async def validate_cedula_ec(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida el slot 'cedula_ec'."""
        
        # Limpia la entrada para quedarse solo con los dígitos.
        cedula_limpia = re.sub(r"[^0-9]", "", str(slot_value))

        # Utiliza la función de validación.
        if validar_cedula_ecuatoriana(cedula_limpia):
            # Si la validación es exitosa, confirma el valor limpio en el slot.
            return {"cedula_ec": cedula_limpia}
        else:
            # Si la validación falla, notifica al usuario y resetea el slot
            # para que el formulario lo pida de nuevo.
            dispatcher.utter_message(text="El número de cédula que ingresó no parece ser válido. Por favor, intente de nuevo.")
            return {"cedula_ec": None}