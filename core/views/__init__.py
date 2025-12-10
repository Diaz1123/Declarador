"""
Vistas de la aplicación core organizadas por módulos.
"""

# Importar funciones auxiliares de sesión
from .declarations import get_session_data, save_session_data

# Vistas del wizard de declaraciones
from .declarations import (
    home,
    step1_identification,
    step2_usage_type,
    step3_details,
    step4_output,
)

# Vistas de descarga
from .downloads import (
    download_text,
    download_json,
)

# Vistas de búsqueda y verificación
from .search import (
    search_declaration,
    view_declaration,
)

# Vistas de firmantes
from .signers import (
    signer_register,
    signer_create,
    signer_verify,
    signers_list,
)

# Vistas auxiliares
from .utils import (
    load_preset,
    preview_declaration,
    save_declaration,
    privacy_policy,
)

__all__ = [
    # Funciones auxiliares
    'get_session_data',
    'save_session_data',
    # Wizard
    'home',
    'step1_identification',
    'step2_usage_type',
    'step3_details',
    'step4_output',
    # Descargas
    'download_text',
    'download_json',
    # Búsqueda
    'search_declaration',
    'view_declaration',
    # Firmantes
    'signer_register',
    'signer_create',
    'signer_verify',
    'signers_list',
    # Auxiliares
    'load_preset',
    'preview_declaration',
    'save_declaration',
    'privacy_policy',
]
