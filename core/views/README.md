# Estructura modular de vistas

Este directorio contiene las vistas de la aplicación organizadas por módulo funcional.

## Archivos

### `declarations.py` (275 líneas)
Vistas del wizard de declaraciones de IA (pasos 1-4):
- `home()` - Landing page
- `step1_identification()` - Paso 1: Checklist diagnóstico
- `step2_usage_type()` - Paso 2: Clasificación de uso
- `step3_details()` - Paso 3: Información detallada
- `step4_output()` - Paso 4: Visualización y descarga
- `get_session_data()` - Helper para datos de sesión
- `save_session_data()` - Helper para guardar sesión

### `downloads.py` (94 líneas)
Vistas para descargar declaraciones en diferentes formatos:
- `download_text()` - Descarga en formato TXT
- `download_json()` - Descarga en formato JSON

### `search.py` (74 líneas)
Vistas para búsqueda y verificación de declaraciones:
- `search_declaration()` - Búsqueda por hash o ID
- `view_declaration()` - Vista de declaración específica

### `signers.py` (134 líneas)
Vistas del módulo de firmantes del compromiso ético:
- `signer_register()` - Formulario de registro
- `signer_create()` - API para crear firmante
- `signer_verify()` - Verificación pública de firma
- `signers_list()` - Lista pública de firmantes

### `utils.py` (184 líneas)
Vistas auxiliares y utilidades:
- `load_preset()` - Cargar plantilla predefinida
- `preview_declaration()` - API de vista previa en tiempo real
- `save_declaration()` - Guardar declaración en BD
- `privacy_policy()` - Política de privacidad

## Beneficios de esta estructura

1. **Mantenibilidad**: Cada archivo tiene <300 líneas, fácil de navegar
2. **Claridad**: Separación clara de responsabilidades
3. **Escalabilidad**: Agregar nuevas funcionalidades sin saturar archivos
4. **Testing**: Más fácil hacer tests unitarios por módulo
5. **Colaboración**: Reduce conflictos en control de versiones

## Migración desde views.py monolítico

Antes: `views.py` (718 líneas)
Después: 5 módulos (832 líneas total, incluyendo imports y docstrings)

El aumento de líneas es mínimo y se debe a:
- Imports duplicados en cada módulo
- Docstrings de módulos
- Mejor documentación
