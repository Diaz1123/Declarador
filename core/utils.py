"""
Utility functions for generating declarations
Migrated from usoeticoia.org utils.ts
"""
import json
import hashlib
import requests
from django.conf import settings
from .constants import USAGE_TYPES, HUMAN_REVIEW_LEVELS, HELP_CHECKLIST, CC_LICENSES
from .translations import (
    get_translation,
    get_translated_usage_types,
    get_translated_review_levels,
    get_translated_content_modes,
    get_translated_checklist
)


def compute_hash(message):
    """Compute SHA-256 hash of a message"""
    hash_obj = hashlib.sha256(message.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    return hash_hex[:16].upper()


def get_usage_label(usage_type, custom_usage_type='', lang='es'):
    """Get label for a usage type"""
    if usage_type == 'other':
        return custom_usage_type or get_translation('usage_other', lang)
    
    # Map usage type values to translation keys
    value_to_key = {
        'draft': 'draft',
        'coauthor': 'coauthor',
        'writing-support': 'writing',
        'ideation': 'ideation',
        'analysis': 'analysis',
        'coding': 'coding',
        'translation': 'translation',
        'review': 'review',
        'other': 'other'
    }
    
    translation_key = value_to_key.get(usage_type, usage_type)
    return get_translation(f'usage_{translation_key}', lang)


def get_review_level_info(level, lang='es'):
    """Get review level information"""
    review_levels = get_translated_review_levels(lang)
    for rl in review_levels:
        if rl['level'] == level:
            return rl
    return None


def get_license_label(license_value, lang='es'):
    """Get license label"""
    # Licenses are usually the same across languages, but we can add translations if needed
    for lic in CC_LICENSES:
        if lic['value'] == license_value:
            return lic['label']
    return license_value


def generate_declaration_text(declaration, hash_value=None, lang='es'):
    """Generate human-readable declaration text"""

    # Parse usage types
    usage_labels = []
    for ut in declaration.usage_types:
        usage_labels.append(get_usage_label(ut, declaration.custom_usage_type, lang))
    usage_text = '; '.join(usage_labels)

    # Parse review level
    review_level = get_review_level_info(declaration.human_review_level, lang)

    # Parse license
    license_label = get_license_label(declaration.license, lang)

    # Parse content modes
    content_modes = []
    translated_modes = get_translated_content_modes(lang)
    
    # Map Spanish modes to translated modes by index
    spanish_modes = [
        'Incorporado tal cual (Verbatim)',
        'Editado parcialmente (ajustes menores)',
        'Reescrito sustancialmente',
        'Usado solo como inspiración/referencia',
        'Sintetizado con otras fuentes',
        'Otro'
    ]
    
    for mode in declaration.content_use_modes:
        if mode == 'Otro' or mode == translated_modes[5]:
            content_modes.append(declaration.custom_content_use_mode or translated_modes[5])
        else:
            # Find index in Spanish modes and use corresponding translated mode
            try:
                index = spanish_modes.index(mode)
                content_modes.append(translated_modes[index])
            except ValueError:
                # If not found, try to find in translated modes
                try:
                    index = translated_modes.index(mode)
                    content_modes.append(mode)  # Already translated
                except ValueError:
                    content_modes.append(mode)  # Fallback to original
    content_modes_text = ', '.join(content_modes)

    # Date string
    date_str = f"{str(declaration.ai_tool_date_month).zfill(2)}/{declaration.ai_tool_date_year}"

    # Diagnostic answers for traceability
    diagnostic_answers = ""
    checklist = get_translated_checklist(lang)
    if declaration.selected_checklist_ids:
        for item_id in declaration.selected_checklist_ids:
            for item in checklist:
                if item['id'] == item_id:
                    diagnostic_answers += f"   [x] {item['q']}\n"
    else:
        diagnostic_answers = f"   ({get_translation('decl_manual_selection', lang)})\n"

    # Build text with translations
    text = f"{get_translation('decl_title', lang)}\n"
    text += "═" * 65 + "\n\n"

    text += f"{get_translation('decl_section_0', lang)}\n"
    text += diagnostic_answers + "\n"

    text += f"{get_translation('decl_section_1', lang)}\n"
    text += f"   {usage_text.upper()}\n\n"

    text += f"{get_translation('decl_section_2', lang)}\n"
    text += f"   {get_translation('decl_tool_name', lang)}: {declaration.ai_tool_name or get_translation('decl_not_specified', lang)}\n"
    text += f"   {get_translation('decl_tool_version', lang)}: {declaration.ai_tool_version or '—'}\n"
    text += f"   {get_translation('decl_tool_provider', lang)}: {declaration.ai_tool_provider or '—'}\n"
    text += f"   {get_translation('decl_tool_date', lang)}: {date_str}\n\n"

    text += f"{get_translation('decl_section_3', lang)}\n"
    text += f"   {declaration.specific_purpose or get_translation('decl_not_described', lang)}\n\n"

    # Prompts
    valid_prompts = [p for p in declaration.prompts if p.get('description', '').strip()]
    if valid_prompts:
        text += f"{get_translation('decl_section_4', lang)}\n"
        for i, p in enumerate(valid_prompts, 1):
            text += f'   {i}. "{p["description"]}"\n'
        text += "\n"

    # Content integration
    if declaration.content_use_modes:
        text += f"{get_translation('decl_section_5', lang)}\n"
        text += f"   {get_translation('decl_content_mode', lang)}: {content_modes_text}\n"
        if declaration.content_use_context:
            text += f"   {get_translation('decl_content_context', lang)}: {declaration.content_use_context}\n"
        text += "\n"

    # Human review
    text += f"{get_translation('decl_section_6', lang)}\n"
    if review_level:
        label_parts = review_level['label'].split(':', 1)
        short_label = label_parts[1].strip() if len(label_parts) > 1 else review_level['label']
        text += f"   {get_translation('decl_review_level', lang)} {declaration.human_review_level}: {short_label}\n"
        text += f"   {get_translation('decl_review_description', lang)}: {review_level['description']}\n"

    if declaration.human_review_level > 0:
        if declaration.reviewer_name:
            text += f"   {get_translation('decl_reviewed_by', lang)}: {declaration.reviewer_name}\n"
        if declaration.reviewer_role:
            text += f"   {get_translation('decl_reviewer_role', lang)}: {declaration.reviewer_role}\n"

    # License
    if declaration.license and declaration.license != 'None':
        text += f"\n{get_translation('decl_section_7', lang)}\n"
        text += f"   • {license_label}\n"

    # Hash validation
    if hash_value:
        text += "\n" + "-" * 65 + "\n"
        text += f"{get_translation('decl_id_registry', lang)}: {declaration.declaration_id}\n"
        text += f"{get_translation('decl_hash_validation', lang)}: {hash_value}\n"

    return text


def generate_declaration_json(declaration, hash_value=None, lang='es'):
    """Generate JSON declaration"""

    # Parse usage types
    usage_labels = []
    for ut in declaration.usage_types:
        usage_labels.append(get_usage_label(ut, declaration.custom_usage_type, lang))

    # Parse review level
    review_level = get_review_level_info(declaration.human_review_level, lang)

    # Parse content modes
    content_modes = []
    translated_modes = get_translated_content_modes(lang)
    
    # Map Spanish modes to translated modes by index
    spanish_modes = [
        'Incorporado tal cual (Verbatim)',
        'Editado parcialmente (ajustes menores)',
        'Reescrito sustancialmente',
        'Usado solo como inspiración/referencia',
        'Sintetizado con otras fuentes',
        'Otro'
    ]
    
    for mode in declaration.content_use_modes:
        if mode == 'Otro' or mode == translated_modes[5]:
            content_modes.append(declaration.custom_content_use_mode or translated_modes[5])
        else:
            # Find index in Spanish modes and use corresponding translated mode
            try:
                index = spanish_modes.index(mode)
                content_modes.append(translated_modes[index])
            except ValueError:
                # If not found, try to find in translated modes
                try:
                    index = translated_modes.index(mode)
                    content_modes.append(mode)  # Already translated
                except ValueError:
                    content_modes.append(mode)  # Fallback to original

    # Valid prompts
    valid_prompts = [p['description'] for p in declaration.prompts if p.get('description', '').strip()]

    payload = {
        'declarationType': 'academic-ai-transparency',
        'version': '4.0.0',
        'generatedAt': declaration.created_at.isoformat() if hasattr(declaration.created_at, 'isoformat') else None,
        'id': declaration.declaration_id,
        'validationHash': hash_value or 'pending',
        'license': declaration.license if declaration.license != 'None' else None,
        'traceability': {
            'diagnosticIds': declaration.selected_checklist_ids
        },
        'usage': {
            'types': declaration.usage_types,
            'labels': usage_labels,
            'customDescription': declaration.custom_usage_type if 'other' in declaration.usage_types else None
        },
        'tool': {
            'name': declaration.ai_tool_name,
            'version': declaration.ai_tool_version,
            'provider': declaration.ai_tool_provider,
            'date': f"{declaration.ai_tool_date_year}-{str(declaration.ai_tool_date_month).zfill(2)}"
        },
        'purpose': declaration.specific_purpose,
        'prompts': valid_prompts,
        'integration': {
            'modes': content_modes,
            'context': declaration.content_use_context or None
        },
        'humanReview': {
            'level': declaration.human_review_level,
            'label': review_level['label'] if review_level else None,
            'description': review_level['description'] if review_level else None,
            'reviewerName': declaration.reviewer_name or None,
            'reviewerRole': declaration.reviewer_role or None
        }
    }

    return json.dumps(payload, ensure_ascii=False, indent=2)


def verify_recaptcha(recaptcha_response, remote_ip=None):
    """
    Verifica el token de reCAPTCHA v2 con la API de Google

    Args:
        recaptcha_response: El token de respuesta del cliente (g-recaptcha-response)
        remote_ip: IP del cliente (opcional pero recomendado)

    Returns:
        dict: {'success': bool, 'error_codes': list, 'score': float}
    """
    # Si reCAPTCHA está deshabilitado, siempre retornar éxito
    if not settings.RECAPTCHA_ENABLED or not settings.RECAPTCHA_SECRET_KEY:
        return {'success': True, 'error_codes': [], 'bypass': True}

    # Si no hay respuesta de reCAPTCHA, fallar
    if not recaptcha_response:
        return {'success': False, 'error_codes': ['missing-input-response']}

    # Preparar datos para la verificación
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response,
    }

    if remote_ip:
        data['remoteip'] = remote_ip

    try:
        # Hacer request a la API de Google reCAPTCHA
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data,
            timeout=5
        )
        result = response.json()

        return {
            'success': result.get('success', False),
            'error_codes': result.get('error-codes', []),
            'challenge_ts': result.get('challenge_ts'),
            'hostname': result.get('hostname'),
        }
    except requests.exceptions.RequestException as e:
        # En caso de error de conexión, registrar y fallar
        return {
            'success': False,
            'error_codes': ['connection-error'],
            'error_message': str(e)
        }
