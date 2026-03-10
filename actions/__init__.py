# Contenido para actions/__init__.py

# Este archivo importa todas las clases de acción desde sus archivos específicos
# para que el servidor de Rasa pueda descubrirlas y registrarlas.

# 1. Importación de acciones globales
from .custom_ask_affirmation import CustomAskAffirmation

# 2. Importación de componentes de acción reutilizables
from .tramites.components.validate_identity_form import ValidateIdentityForm

# 3. Importación de los orquestadores de cada trámite
from .tramites.residencia_individual.residencia_individual import ResidenciaIndividual
from .tramites.residencia_grupal.residencia_grupal import ResidenciaGrupal