"""
Vistas auxiliares (presets, preview, privacy, etc).
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.translation import get_language
from datetime import datetime
import json as json_lib
import traceback

from ..models import Declaration
from ..constants import PRESETS
from ..utils import generate_declaration_text
from ..translations import get_translated_glossary
from .declarations import get_session_data, save_session_data


@require_http_methods(["POST"])
def load_preset(request):
    """Load a preset template"""
    preset_id = request.POST.get('preset_id')

    for preset in PRESETS:
        if preset['id'] == preset_id:
            data = get_session_data(request)
            preset_data = preset['data']

            # Update session data with preset
            data['usage_types'] = preset_data.get('usage_types', [])
            data['specific_purpose'] = preset_data.get('specific_purpose', '')
            data['content_use_modes'] = preset_data.get('content_use_modes', [])
            data['human_review']['level'] = preset_data.get('human_review_level', 0)
            data['human_review']['reviewer_role'] = preset_data.get('reviewer_role', '')

            save_session_data(request, data)

            # Jump to step 3 (details)
            return redirect('step3')

    return redirect('step1')


@require_http_methods(["POST"])
def preview_declaration(request):
    """API endpoint para generar vista previa en tiempo real"""
    try:
        # Obtener datos del cuerpo de la petición
        form_data = json_lib.loads(request.body)
        current_lang = get_language()

        # Obtener datos de la sesión como base (para datos de pasos anteriores)
        session_data = get_session_data(request)

        # Combinar datos: usar los del formulario si están disponibles, sino usar los de la sesión
        merged_data = {
            'selected_checklist_ids': form_data.get('selected_checklist_ids') if 'selected_checklist_ids' in form_data else session_data.get('selected_checklist_ids', []),
            'usage_types': form_data.get('usage_types') if 'usage_types' in form_data else session_data.get('usage_types', []),
            'custom_usage_type': form_data.get('custom_usage_type') if 'custom_usage_type' in form_data else session_data.get('custom_usage_type', ''),
            'ai_tool': {
                'name': form_data.get('ai_tool', {}).get('name') if 'ai_tool' in form_data and 'name' in form_data.get('ai_tool', {}) else session_data.get('ai_tool', {}).get('name', ''),
                'version': form_data.get('ai_tool', {}).get('version') if 'ai_tool' in form_data and 'version' in form_data.get('ai_tool', {}) else session_data.get('ai_tool', {}).get('version', ''),
                'provider': form_data.get('ai_tool', {}).get('provider') if 'ai_tool' in form_data and 'provider' in form_data.get('ai_tool', {}) else session_data.get('ai_tool', {}).get('provider', ''),
                'date_month': form_data.get('ai_tool', {}).get('date_month') if 'ai_tool' in form_data and 'date_month' in form_data.get('ai_tool', {}) else session_data.get('ai_tool', {}).get('date_month', datetime.now().month),
                'date_year': form_data.get('ai_tool', {}).get('date_year') if 'ai_tool' in form_data and 'date_year' in form_data.get('ai_tool', {}) else session_data.get('ai_tool', {}).get('date_year', datetime.now().year),
            },
            'specific_purpose': form_data.get('specific_purpose') if 'specific_purpose' in form_data else session_data.get('specific_purpose', ''),
            'prompts': form_data.get('prompts') if 'prompts' in form_data else session_data.get('prompts', []),
            'content_use_modes': form_data.get('content_use_modes') if 'content_use_modes' in form_data else session_data.get('content_use_modes', []),
            'custom_content_use_mode': form_data.get('custom_content_use_mode') if 'custom_content_use_mode' in form_data else session_data.get('custom_content_use_mode', ''),
            'content_use_context': form_data.get('content_use_context') if 'content_use_context' in form_data else session_data.get('content_use_context', ''),
            'human_review': {
                'level': form_data.get('human_review', {}).get('level') if 'human_review' in form_data and 'level' in form_data.get('human_review', {}) else session_data.get('human_review', {}).get('level', 0),
                'reviewer_name': form_data.get('human_review', {}).get('reviewer_name') if 'human_review' in form_data and 'reviewer_name' in form_data.get('human_review', {}) else session_data.get('human_review', {}).get('reviewer_name', ''),
                'reviewer_role': form_data.get('human_review', {}).get('reviewer_role') if 'human_review' in form_data and 'reviewer_role' in form_data.get('human_review', {}) else session_data.get('human_review', {}).get('reviewer_role', ''),
            },
            'license': form_data.get('license') if 'license' in form_data else session_data.get('license', 'None')
        }

        # Crear objeto Declaration temporal para generar la vista previa
        declaration = Declaration(
            selected_checklist_ids=merged_data['selected_checklist_ids'],
            usage_types=merged_data['usage_types'],
            custom_usage_type=merged_data['custom_usage_type'],
            ai_tool_name=merged_data['ai_tool']['name'],
            ai_tool_version=merged_data['ai_tool']['version'],
            ai_tool_provider=merged_data['ai_tool']['provider'],
            ai_tool_date_month=merged_data['ai_tool']['date_month'],
            ai_tool_date_year=merged_data['ai_tool']['date_year'],
            specific_purpose=merged_data['specific_purpose'],
            prompts=merged_data['prompts'],
            content_use_modes=merged_data['content_use_modes'],
            custom_content_use_mode=merged_data['custom_content_use_mode'],
            content_use_context=merged_data['content_use_context'],
            human_review_level=merged_data['human_review']['level'],
            reviewer_name=merged_data['human_review']['reviewer_name'],
            reviewer_role=merged_data['human_review']['reviewer_role'],
            license=merged_data['license']
        )

        # Generar vista previa sin hash (ya que aún no está finalizada)
        preview_text = generate_declaration_text(declaration, None, current_lang)

        return JsonResponse({
            'success': True,
            'preview': preview_text
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=400)


@require_http_methods(["POST"])
def save_declaration(request):
    """Guardar la declaración generada en la base de datos (opcional)"""
    try:
        data = get_session_data(request)
        current_lang = get_language()

        # Verificar si ya hay una declaración generada
        if 'generated_declaration' not in request.session:
            return JsonResponse({
                'success': False,
                'error': 'No hay una declaración generada para guardar'
            }, status=400)

        # Crear y guardar la declaración
        declaration = Declaration(
            selected_checklist_ids=data.get('selected_checklist_ids', []),
            usage_types=data.get('usage_types', []),
            custom_usage_type=data.get('custom_usage_type', ''),
            ai_tool_name=data['ai_tool']['name'],
            ai_tool_version=data['ai_tool']['version'],
            ai_tool_provider=data['ai_tool']['provider'],
            ai_tool_date_month=data['ai_tool']['date_month'],
            ai_tool_date_year=data['ai_tool']['date_year'],
            specific_purpose=data.get('specific_purpose', ''),
            prompts=data.get('prompts', []),
            content_use_modes=data.get('content_use_modes', []),
            custom_content_use_mode=data.get('custom_content_use_mode', ''),
            content_use_context=data.get('content_use_context', ''),
            human_review_level=data['human_review']['level'],
            reviewer_name=data['human_review']['reviewer_name'],
            reviewer_role=data['human_review']['reviewer_role'],
            license=data.get('license', 'None')
        )

        # Usar los datos generados previamente
        generated = request.session['generated_declaration']
        declaration.declaration_id = generated['declaration_id']
        declaration.validation_hash = generated['validation_hash']

        # Guardar en la base de datos
        declaration.save()

        # Marcar como guardado en sesión
        request.session['declaration_saved'] = True
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'message': 'Declaración guardada exitosamente',
            'declaration_id': declaration.declaration_id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


def privacy_policy(request):
    """Política de privacidad"""
    current_lang = get_language()

    context = {
        'glossary': get_translated_glossary(current_lang),
    }
    return render(request, 'core/privacy.html', context)
