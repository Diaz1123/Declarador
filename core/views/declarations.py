"""
Vistas del wizard de declaraciones (pasos 1-4).
"""
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import get_language
from datetime import datetime
import random
import string

from ..models import Declaration
from ..constants import (
    HELP_CHECKLIST, PRESETS, MONTHS_ES, AI_TOOLS_CATALOG, FIELD_LIMITS, CC_LICENSES
)
from ..utils import (
    generate_declaration_text,
    generate_declaration_json,
    compute_hash
)
from ..translations import (
    get_translated_usage_types,
    get_translated_steps_labels,
    get_translated_checklist,
    get_translated_content_modes,
    get_translated_review_levels,
    get_translated_glossary
)


def get_session_data(request):
    """Get or initialize session data for the wizard"""
    if 'declaration_data' not in request.session or request.session['declaration_data'] is None:
        request.session['declaration_data'] = {
            'current_step': 0,
            'ai_used': True,  # By default, assume AI was used
            'selected_checklist_ids': [],
            'usage_types': [],
            'custom_usage_type': '',
            'ai_tool': {
                'name': '',
                'version': '',
                'provider': '',
                'date_month': datetime.now().month,
                'date_year': datetime.now().year
            },
            'specific_purpose': '',
            'prompts': [{'id': '1', 'description': ''}],
            'content_use_modes': [],
            'custom_content_use_mode': '',
            'content_use_context': '',
            'human_review': {
                'level': 0,
                'reviewer_role': '',
                'reviewer_name': ''
            },
            'license': 'None',
            'author_name': '',
            'author_email': ''
        }
    return request.session['declaration_data']


def save_session_data(request, data):
    """Save data to session"""
    request.session['declaration_data'] = data
    request.session.modified = True


def home(request):
    """Landing page - redirects to step 1"""
    # Reset session data on new visit
    if 'reset' in request.GET:
        if 'declaration_data' in request.session:
            del request.session['declaration_data']
        if 'generated_declaration' in request.session:
            del request.session['generated_declaration']
        if 'declaration_saved' in request.session:
            del request.session['declaration_saved']
    return redirect('step1')


def step1_identification(request):
    """Step 1: Diagnostic checklist"""
    data = get_session_data(request)
    current_lang = get_language()

    if request.method == 'POST':
        # Verificar reCAPTCHA si está habilitado
        from django.conf import settings
        from ..utils import verify_recaptcha

        if settings.RECAPTCHA_ENABLED:
            # Verificar si ya fue validado en esta sesión
            if not request.session.get('recaptcha_verified_step1', False):
                recaptcha_response = request.POST.get('g-recaptcha-response')
                remote_ip = request.META.get('REMOTE_ADDR')

                verification = verify_recaptcha(recaptcha_response, remote_ip)

                # Log para debug
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"reCAPTCHA verification: {verification}")
                logger.error(f"reCAPTCHA response: {recaptcha_response}")
                logger.error(f"Remote IP: {remote_ip}")

                if not verification['success']:
                    # reCAPTCHA falló
                    from django.contrib import messages
                    error_msg = 'Por favor completa la verificación reCAPTCHA.'
                    if verification.get('error_codes'):
                        error_msg += f" Códigos: {', '.join(verification['error_codes'])}"
                    messages.error(request, error_msg)
                    return render(request, 'core/step1_identification.html', {
                        'step': 0,
                        'steps_labels': get_translated_steps_labels(current_lang),
                        'checklist': get_translated_checklist(current_lang),
                        'selected_ids': data.get('selected_checklist_ids', []),
                        'glossary': get_translated_glossary(current_lang),
                    })

                # Marcar como verificado en la sesión
                request.session['recaptcha_verified_step1'] = True

        # Check if "No AI used" option was selected
        no_ai_used = request.POST.get('no_ai_used') == 'true'
        data['ai_used'] = not no_ai_used

        if no_ai_used:
            # If no AI was used, skip directly to step 4 with minimal data
            data['selected_checklist_ids'] = []
            data['usage_types'] = []
            data['current_step'] = 3  # Go directly to output
            save_session_data(request, data)
            return redirect('step4')

        # Get selected checklist items (only if AI was used)
        selected_ids = request.POST.getlist('checklist')
        data['selected_checklist_ids'] = selected_ids

        # Determine dominant usage type
        if selected_ids:
            # Get items sorted by priority
            selected_items = [item for item in HELP_CHECKLIST if item['id'] in selected_ids]
            selected_items.sort(key=lambda x: x['priority'], reverse=True)
            if selected_items:
                data['usage_types'] = [selected_items[0]['suggests']]

        data['current_step'] = 1
        save_session_data(request, data)
        return redirect('step2')

    context = {
        'step': 0,
        'steps_labels': get_translated_steps_labels(current_lang),
        'checklist': get_translated_checklist(current_lang),
        'selected_ids': data.get('selected_checklist_ids', []),
        'no_ai_used': not data.get('ai_used', True),
        'glossary': get_translated_glossary(current_lang),
        'presets': PRESETS,
    }
    return render(request, 'core/step1_identification.html', context)


def step2_usage_type(request):
    """Step 2: Usage type classification"""
    data = get_session_data(request)
    current_lang = get_language()

    if request.method == 'POST':
        # Check if user wants to go back
        if 'back' in request.POST:
            return redirect('step1')

        # Get selected usage types
        usage_types = request.POST.getlist('usage_types')
        data['usage_types'] = usage_types
        data['custom_usage_type'] = request.POST.get('custom_usage_type', '')

        data['current_step'] = 2
        save_session_data(request, data)
        return redirect('step3')

    context = {
        'step': 1,
        'steps_labels': get_translated_steps_labels(current_lang),
        'usage_types_list': get_translated_usage_types(current_lang),
        'selected_types': data.get('usage_types', []),
        'custom_usage_type': data.get('custom_usage_type', ''),
        'glossary': get_translated_glossary(current_lang),
        'presets': PRESETS,
    }
    return render(request, 'core/step2_usage_type.html', context)


def step3_details(request):
    """Step 3: Detailed information"""
    data = get_session_data(request)
    current_lang = get_language()

    if request.method == 'POST':
        # Check if user wants to go back
        if 'back' in request.POST:
            return redirect('step2')

        # Verificar reCAPTCHA si está habilitado y no fue verificado en paso 1
        from django.conf import settings
        from ..utils import verify_recaptcha

        if settings.RECAPTCHA_ENABLED:
            # Verificar si ya fue validado en paso 1
            if not request.session.get('recaptcha_verified_step1', False):
                recaptcha_response = request.POST.get('g-recaptcha-response')
                remote_ip = request.META.get('REMOTE_ADDR')

                verification = verify_recaptcha(recaptcha_response, remote_ip)

                # Log para debug
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"reCAPTCHA Step 3 verification: {verification}")

                if not verification['success']:
                    # reCAPTCHA falló
                    from django.contrib import messages
                    error_msg = 'Por favor completa la verificación reCAPTCHA.'
                    if verification.get('error_codes'):
                        error_msg += f" Códigos: {', '.join(verification['error_codes'])}"
                    messages.error(request, error_msg)

                    # Volver a renderizar el formulario con los datos ingresados
                    context = {
                        'step': 2,
                        'steps_labels': get_translated_steps_labels(current_lang),
                        'data': data,
                        'content_use_modes': get_translated_content_modes(current_lang),
                        'review_levels': get_translated_review_levels(current_lang),
                        'licenses': CC_LICENSES,
                        'months': MONTHS_ES,
                        'years': range(2023, 2027),
                        'glossary': get_translated_glossary(current_lang),
                        'presets': PRESETS,
                        'ai_tools_catalog': AI_TOOLS_CATALOG,
                        'field_limits': FIELD_LIMITS,
                        'recaptcha_verified': False,
                    }
                    return render(request, 'core/step3_details.html', context)

        # AI Tool info
        data['ai_tool'] = {
            'name': request.POST.get('ai_tool_name', ''),
            'version': request.POST.get('ai_tool_version', ''),
            'provider': request.POST.get('ai_tool_provider', ''),
            'date_month': int(request.POST.get('ai_tool_date_month', datetime.now().month)),
            'date_year': int(request.POST.get('ai_tool_date_year', datetime.now().year))
        }

        # Purpose
        data['specific_purpose'] = request.POST.get('specific_purpose', '')

        # Prompts - parse from form
        prompts = []
        prompt_counter = 0
        while f'prompt_{prompt_counter}' in request.POST:
            desc = request.POST.get(f'prompt_{prompt_counter}', '').strip()
            if desc:
                prompts.append({'id': str(prompt_counter), 'description': desc})
            prompt_counter += 1
        if not prompts:
            prompts = [{'id': '0', 'description': ''}]
        data['prompts'] = prompts

        # Content integration
        data['content_use_modes'] = request.POST.getlist('content_use_modes')
        data['custom_content_use_mode'] = request.POST.get('custom_content_use_mode', '')
        data['content_use_context'] = request.POST.get('content_use_context', '')

        # Human review
        data['human_review'] = {
            'level': int(request.POST.get('human_review_level', 0)),
            'reviewer_name': request.POST.get('reviewer_name', ''),
            'reviewer_role': request.POST.get('reviewer_role', '')
        }

        # License
        data['license'] = request.POST.get('license', 'None')

        data['current_step'] = 3
        save_session_data(request, data)
        return redirect('step4')

    context = {
        'step': 2,
        'steps_labels': get_translated_steps_labels(current_lang),
        'data': data,
        'content_use_modes': get_translated_content_modes(current_lang),
        'review_levels': get_translated_review_levels(current_lang),
        'licenses': CC_LICENSES,
        'months': MONTHS_ES,
        'years': range(2023, 2027),
        'glossary': get_translated_glossary(current_lang),
        'presets': PRESETS,
        'ai_tools_catalog': AI_TOOLS_CATALOG,
        'field_limits': FIELD_LIMITS,
        'recaptcha_verified': request.session.get('recaptcha_verified_step1', False),
    }
    return render(request, 'core/step3_details.html', context)


@ensure_csrf_cookie
def step4_output(request):
    """Step 4: Display and download declaration"""
    data = get_session_data(request)
    current_lang = get_language()

    # Create Declaration object (but don't save yet)
    declaration = Declaration(
        ai_used=data.get('ai_used', True),
        selected_checklist_ids=data.get('selected_checklist_ids', []),
        usage_types=data.get('usage_types', []),
        custom_usage_type=data.get('custom_usage_type', ''),
        ai_tool_name=data.get('ai_tool', {}).get('name', ''),
        ai_tool_version=data.get('ai_tool', {}).get('version', ''),
        ai_tool_provider=data.get('ai_tool', {}).get('provider', ''),
        ai_tool_date_month=data.get('ai_tool', {}).get('date_month', datetime.now().month),
        ai_tool_date_year=data.get('ai_tool', {}).get('date_year', datetime.now().year),
        specific_purpose=data.get('specific_purpose', ''),
        prompts=data.get('prompts', []),
        content_use_modes=data.get('content_use_modes', []),
        custom_content_use_mode=data.get('custom_content_use_mode', ''),
        content_use_context=data.get('content_use_context', ''),
        human_review_level=data.get('human_review', {}).get('level', 0),
        reviewer_name=data.get('human_review', {}).get('reviewer_name', ''),
        reviewer_role=data.get('human_review', {}).get('reviewer_role', ''),
        license=data.get('license', 'None')
    )

    # Generate ID for display
    declaration.declaration_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # Generate text and hash
    text_output = generate_declaration_text(declaration, None, current_lang)
    hash_value = compute_hash(text_output)
    declaration.validation_hash = hash_value

    # Generate final outputs
    text_output = generate_declaration_text(declaration, hash_value, current_lang)
    json_output = generate_declaration_json(declaration, hash_value, current_lang)

    # Guardar en sesión para guardado posterior opcional
    request.session['generated_declaration'] = {
        'declaration_id': declaration.declaration_id,
        'validation_hash': hash_value,
        'text_output': text_output,
        'json_output': json_output,
    }
    request.session.modified = True

    # Verificar si ya se guardó anteriormente
    is_saved = request.session.get('declaration_saved', False)

    context = {
        'step': 3,
        'steps_labels': get_translated_steps_labels(current_lang),
        'declaration': declaration,
        'text_output': text_output,
        'json_output': json_output,
        'hash': hash_value,
        'glossary': get_translated_glossary(current_lang),
        'presets': PRESETS,
        'is_saved': is_saved,
    }
    return render(request, 'core/step4_output.html', context)
