"""
Vistas para descargar declaraciones en diferentes formatos.
"""
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.translation import get_language
from datetime import datetime
import random
import string

from ..models import Declaration
from ..utils import (
    generate_declaration_text,
    generate_declaration_json,
    compute_hash
)
from .declarations import get_session_data


@require_http_methods(["GET"])
def download_text(request):
    """Download declaration as text file"""
    data = get_session_data(request)
    current_lang = get_language()

    # Create Declaration object
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

    declaration.declaration_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    text_output = generate_declaration_text(declaration, None, current_lang)
    hash_value = compute_hash(text_output)
    text_output = generate_declaration_text(declaration, hash_value, current_lang)

    response = HttpResponse(text_output, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="declaracion-ia-v4.txt"'
    return response


@require_http_methods(["GET"])
def download_json(request):
    """Download declaration as JSON file"""
    data = get_session_data(request)
    current_lang = get_language()

    # Create Declaration object
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

    declaration.declaration_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    declaration.created_at = datetime.now()

    text_output = generate_declaration_text(declaration, None, current_lang)
    hash_value = compute_hash(text_output)
    json_output = generate_declaration_json(declaration, hash_value, current_lang)

    response = HttpResponse(json_output, content_type='application/json; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="declaracion-ia-v4.json"'
    return response
